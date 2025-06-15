from answer import answering, insert
import chromadb
from insert import get_doc_insert
from tqdm.notebook import tqdm

if __name__ == '__main__':
    while True:
        query = input("ask me somethings:")
        if query == "quit":
            print(f"Answer: see you again")
            break
        ans, data = answering(query)
        print(ans)