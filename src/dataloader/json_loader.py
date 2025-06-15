import langchain
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from pymongo import MongoClient
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os
import pandas
import numpy
import json
# from tqdm.notebook import tqdm

def config_bh(inp):
    inp = str(inp)
    inp = inp.replace('{', '')
    inp = inp.replace('}', '')
    inp = inp.replace("'", '')
    if inp == '':
        return 'no information'
    return inp

def config_review(inp):
    try:
        data = pandas.DataFrame(inp).review_content.values
        rvs = ''
        for i, rv in enumerate(data):
            if rv != '':
                rvs += f'review {i + 1}: ' + rv + '\n'
        rvs = llm.invoke(f"""{rvs} 
        only answer my question, do not give more information, sort and accurate
        summary all the reviews above less than 100 words.
        """)
        rvs = rvs.content
        return rvs
    except:
        return 'no information'

def get_json_loader(folder='data/'):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 50)
    datas = os.listdir(folder)
    mtdocs = []
    for f in datas:
        with open(folder + f) as file:
            dt = json.load(file)
            dt = pandas.DataFrame(dt)
            name = dt.name.values
            address = dt.address.values
            business_hours = dt.business_hours.values
            phones = dt.phone_number.values
            avg_rate = dt.rate.values
            reviews = dt.reviews.values
            photo_link = dt.photo_link.values
            tp = dt.type.values
            location = dt.location.values
        docs = []
        print('load restaurant')
        for i in range(len(name)):
            print(f'res {i + 1}')
            info = f"""
            name: {name[i]},
            address: {address[i]}
            time: {config_bh(business_hours[i])}
            phone number: {phones[i]}
            avg rate: {avg_rate[i] if avg_rate[i] != '' else 'no information'}
            sort review: {config_review(reviews[i])}
            type: {tp[i]}
            location: {location[i]}
            """
            docs.append([info, {'images': list(photo_link)}])
        mtdocs.append(docs)
    return mtdocs

if __name__ == "__main__":
    print(len(get_json_loader()))
   