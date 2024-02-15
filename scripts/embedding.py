from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
import os
import shutil
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceInstructEmbeddings

CHROMA_PATH = "chroma"
DATA_PATH = "content"

def generate_data_store(model_name="hkunlp/instructor-base"):
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks, model_name)

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.txt", show_progress=False)
    documents = loader.load()
    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

def save_to_chroma(chunks, model_name):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    embeddings = HuggingFaceInstructEmbeddings(model_name=model_name)
    db = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH)
    db.persist()
    db = None
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
