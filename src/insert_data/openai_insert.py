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
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from src.utils.utils import *

CUR_DIR = os.getcwd()
logging.info("working directory: " + CUR_DIR)

os.environ['OPENAI_API_KEY'] = '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'

client = chromadb.PersistentClient(path=os.path.join(CUR_DIR,"chromadb/"))


openai_embed =  OpenAIEmbeddings(model="text-embedding-3-large")


RAW_DIR = os.path.join(CUR_DIR, "data/raw_docs")
logging.info("raw directory: " + RAW_DIR)



raw_documents = []
filenames = get_files(RAW_DIR)

for filename in filenames:
    raw_documents.extend(Docx2txtLoader(filename).load())
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

openai_lc_client = Chroma.from_documents(
    documents, openai_embed, client=client, collection_name="openai_context"
)