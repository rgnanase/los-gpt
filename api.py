import os
from dotenv import dotenv_values
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import uvicorn
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
import pandas as pd
import matplotlib.pyplot as plt
import tiktoken

app = Starlette()
app.mount("/docs", StaticFiles(directory="docs"), name="docs")
app = FastAPI()
env_vars = dotenv_values('.env')
os.environ["OPENAI_API_KEY"] = env_vars['OPENAI_API_KEY']
def count_tokens(text: str) -> int:
    return len(tiktoken.encoding_for_model("gpt-4").encode(text))
@app.on_event("startup")
async def start_databases():
    start_openai_db()
def start_openai_db():
    print("Reindexing openai database")
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    with open('LoS_Domestic_updated_sale_upd.txt', 'r', encoding="utf-8") as f:
        text = f.read()
    # Step 3: Create function to count tokens
    print(count_tokens(text))
    # Step 4: Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=350,
        chunk_overlap=24,
        length_function=count_tokens,
    )
    chunks = text_splitter.create_documents([text])
    # Add new key-value pair to each dictionary
    for i in range(len(chunks)):
        chunks[i].metadata = {
            "metadata": str(i)
        }
    print(chunks[1])
    # Create a list of token counts
    token_counts = [count_tokens(chunk.page_content) for chunk in chunks]
    # Create a DataFrame from the token counts
    df = pd.DataFrame({'Token Count': token_counts})
    # Create a histogram of the token count distribution
    df.hist(bins=40, )
    # Show the plot
    plt.show()
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(chunks, embedding=embeddings,
                                     persist_directory="db_openai")
    vectordb.persist()
    from langchain.chains import ConversationalRetrievalChain
    from langchain.memory import ConversationBufferMemory
    from langchain.llms import OpenAI
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    global bot
    bot = ConversationalRetrievalChain.from_llm(OpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.8),
                                                vectordb.as_retriever(), memory=memory, verbose='true')

@app.post("/send_openai")
async def send_openai(text: str = Body(..., embed=True)):
    print(f'Input to AI model: {text}')
    response = bot.run(text)
    print(f'Response from OpenAI model: {response}')
    return JSONResponse(content=response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
