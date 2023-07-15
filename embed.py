import os
from dotenv import dotenv_values
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import tiktoken
from langchain.text_splitter import CharacterTextSplitter
import json

env_vars = dotenv_values('.env')
os.environ["OPENAI_API_KEY"] = env_vars['OPENAI_API_KEY']

openai_embeddings = OpenAIEmbeddings(openai_api_key=env_vars['OPENAI_API_KEY'], model="text-embedding-ada-002")


def count_tokens(documents):
    # Cost of text-embedding-ada-002 is $0.03 / 1K tokens
    total_tokens = sum(
        len(tiktoken.encoding_for_model("gpt-4").encode(document.page_content)) for document in
        documents)
    print("Total tokens:", total_tokens, "\nTotal cost of tokens: $", total_tokens * 0.03 / 1000)


if not os.path.exists("db_openai_chroma"):
    # print('Load TOC to create metadata for sources')
    # with open("pages_html/scrape_toc.json", "r") as json_file:
    #     scrape_toc_data = json.load(json_file)

    from langchain.document_loaders import DirectoryLoader
    loader = DirectoryLoader('./docs', glob="**/*.txt")
    documents = loader.load()
    texts = []
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=24, separators=["\n"])
    texts = text_splitter.split_documents(documents)

    print('Recreating database and embeddings')
    # directory = "pages_txt"
    # files = [file for file in os.listdir(directory) if file.endswith(".txt")]

    # text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=24)

    # print('Parsing documents')
    #
    # documents = []
    # for file in files:
    #     with open(os.path.join(directory, file), "r", encoding="utf-8") as f:
    #         matching_entry_in_toc_json = next((entry for entry in scrape_toc_data if entry['file_name'] == file), None)
    #         metadatas = [{"source": f'{matching_entry_in_toc_json["title"]}-{matching_entry_in_toc_json["url"]}'}]
    #         texts = text_splitter.create_documents([f.read()], metadatas=metadatas)
    #         documents.extend(texts)

    # count_tokens(documents)
    count_tokens(texts)
    print('Creating embeddings')
    db = Chroma.from_documents(texts, embedding=openai_embeddings, persist_directory="db_openai_chroma")
else:
    print("Delete the db_openai_chroma first if you want to rebuild the database embeddings")

