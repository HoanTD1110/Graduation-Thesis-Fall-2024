import sys
sys.path.append('./')
import logging
import chromadb
import os
import glob
from langchain.document_loaders import (
    TextLoader,
    DataFrameLoader,
    UnstructuredWordDocumentLoader,
    Docx2txtLoader,
)
from langchain.text_splitter import CharacterTextSplitter

logging.basicConfig(level=logging.DEBUG)
from chromadb.utils import embedding_functions

from src.utils.utils import *

CUR_DIR = os.getcwd()
logging.info("working directory: " + CUR_DIR)

client = chromadb.PersistentClient(path=os.path.join(CUR_DIR,"chromadb/"))

try:
    default_ef = embedding_functions.DefaultEmbeddingFunction()
    collection = client.create_collection(name="default_context", 
                                          embedding_function=default_ef)
    memory = client.create_collection(name="default_memory", 
                                          embedding_function=default_ef)
except:
    collection = client.get_collection(name="default_context", 
                                          embedding_function=default_ef)
    memory = client.get_collection(name="default_memory", 
                                          embedding_function=default_ef)


RAW_DIR = os.path.join(CUR_DIR, "data/raw_docs")
logging.info("raw directory: " + RAW_DIR)

raw_documents = []
filenames = get_files(RAW_DIR)

for filename in filenames:
    raw_documents.extend(Docx2txtLoader(filename).load())
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)
count = 0
print(collection)
for doc in documents:
    count += 1
    collection.add(
        documents=[str(doc.page_content)],
        metadatas=[{'a': 'a'}],
        ids=[str(count)]
    )