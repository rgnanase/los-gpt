#!/usr/bin/env python3
from typing import List, Tuple

from nicegui import app, Client, ui
from nicegui.events import ValueChangeEventArguments

messages: List[Tuple[str, str, str]] = []
thinking: bool = False

app.add_static_files('/docs', 'docs')

llm = None
using_local_llm = False


def init_openai_db():
    import os
    os.environ["OPENAI_API_KEY"] = "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"

    from langchain.document_loaders import PyPDFDirectoryLoader
    loader = PyPDFDirectoryLoader("./docs")
    documents = loader.load_and_split()
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma
    from langchain.chains import ConversationalRetrievalChain
    from langchain.memory import ConversationBufferMemory
    from langchain.llms import OpenAI

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents, embedding=embeddings,
                                     persist_directory="db-openai")
    vectordb.persist()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    global llm
    llm = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.8), vectordb.as_retriever(), memory=memory)


init_openai_db()


def init_local_db():
    from langchain.document_loaders import PyPDFDirectoryLoader
    loader = PyPDFDirectoryLoader("./docs")
    documents = loader.load_and_split()
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
    texts = text_splitter.split_documents(documents)
    from langchain.embeddings import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    from langchain.vectorstores import Chroma
    db = Chroma.from_documents(texts, embeddings, persist_directory="db_local")
    from langchain.llms import GPT4All
    model_path = "./ggml-gpt4all-j-v1.3-groovy.bin"

    model = GPT4All(model=model_path, n_ctx=1000, backend="gptj", verbose=False)
    from langchain.chains import RetrievalQA
    global llm
    llm = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=False,
        verbose=False
    )


def switch_model(event: ValueChangeEventArguments):
    global using_local_llm
    global messages
    if event.value == 'GPT 3.5':
        messages = []
        chat_messages.refresh()
        init_openai_db()
        using_local_llm = False
        ui.notify(f'Switched to GPT 3.5 model')
    else:
        messages = []
        chat_messages.refresh()
        init_local_db()
        using_local_llm = True
        ui.notify(f'Switched to local model')


@ui.refreshable
async def chat_messages() -> None:
    for name, text in messages:
        ui.chat_message(text=text, name=name, sent=name == 'You')
    if thinking:
        ui.spinner(size='3rem').classes('self-center')
    await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)', respond=False)


@ui.page('/')
async def main(client: Client):
    async def send() -> None:
        global thinking
        message = text.value
        messages.append(('You', text.value))
        thinking = True
        text.value = ''
        chat_messages.refresh()
        if using_local_llm:
            chat_messages.refresh()
            import time
            time.sleep(1)
            response = llm.run(message)
        else:
            response = await llm.arun(message)
        messages.append(('Bot', response))
        thinking = False
        chat_messages.refresh()

    anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
    ui.add_head_html(f'<style>{anchor_style}</style>')
    await client.connected()

    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        ai_model = ui.radio(['GPT 3.5', 'Local'], value='GPT 3.5', on_change=switch_model).props('inline')
        ui.markdown(
            'The Vector database has indexed the [Overview](docs/Billing Overview Student Financial Services and Cashiering.pdf), [Schedule](docs/Billing Schedule Student Financial Services and Cashiering.pdf), and [Fees](docs/Tuition and Fees Student Financial Services and Cashiering.pdf) PDF documents. Review these documents for questions you can ask')

    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        await chat_messages()

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            text = ui.input().props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')


ui.run(title='Chat with GPT-3 (example)')
