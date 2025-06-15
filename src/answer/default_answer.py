import sys
sys.path.append('./')
import langchain
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from chromadb.utils import embedding_functions
from src.dataloader.json_loader import get_json_loader
import chromadb
import os
import pandas
import numpy
import json
from tqdm.notebook import tqdm

CUR_DIR = os.getcwd()

os.environ['OPENAI_API_KEY'] = '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'

client = chromadb.PersistentClient(path=os.path.join(CUR_DIR,"chromadb/"))
llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k-0613")

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

#promt engineering. (need 1)
def answering_no_memory(query, data, mem=''):
    context=data
    
    promt = f"""
    ### Instruction: You're a information support agent that is talking to a customer. Use only the chat history and the following information
    {context}
    nếu hỏi các bước thì hãy đưa ra các bước cụ thể, thông tin chỉ được phép lấy từ trong phần thông tin bên trên.
    nếu hỏi tư vấn về sản phẩm hay dịch vụ thì hãy tư vấn dựa trên các thông tin người dùng cung cấp và áp dụng với các điều kiện và chính sách của sản phẩm để tư vấn
    với những câu hỏi so sánh với dữ liệu trong docs, hãy lấy những dữ liệu liên quan đến câu hỏi rồi so sánh chúng với nhau
    với những câu hỏi tư vấn, nếu khách hàng không đưa được đủ các thông tin yêu cầu của đối tượng áp dụng hay sản phẩm, hãy đưa ra lời tư vấn match theo những thông tin được khách hàng cung cấp, đối chiếu với những thông tin trong sản phẩm để đưa ra các sản phẩm hoặc thông tin tư vấn
    to answer in a helpful manner to the question. If you don't know the answer - say that you don't know.
    Keep your replies short, compassionate and informative.
    {mem}
    ### Input: {query}
    ### Response:
    """
    op = llm.invoke(promt).content
    return op

def answering(query):
    out = collection.query(
        query_texts=[query],
        n_results=5,
    )
    mem = memory.query(
        query_texts=[query],
        n_results=5
    )
    #get data.
    # print('data query:', out)
    data = out['documents'][0]
    data = '\n\n'.join(data)
    #get memory.
    mem = mem['documents'][0]
    mem = '\n\n'.join(data)
    #answering.
    answer = answering_no_memory(query, data, mem=mem)
    #insert into memory.
    memory.add(
        documents=[f"user question: {query}", f"GODA AI answer: {answer}"],
        metadatas=[{'time': 'time'}, {'time': 'time'}],
        ids=[query, answer]
    )
    for key in out.keys():
        try:
            out[key] = out[key][0]
        except:
            continue
    return answer, data

def insert():
    mtdocs = get_json_loader()
    count = 0
    for docs in mtdocs:
        for f in tqdm(docs):
            count += 1
            collection.add(
                documents=[f[0]],
                metadatas=[{'images': '\n'.join(f[1]['images'])}],
                ids=[str(count)]
            )