import openai
import pinecone
from tqdm import tqdm
import os
import pickle
import sqlite3
from sqlite3 import Error

#initialize pinecone connection
index_name = 'article-vectors-ada'

# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment="us-east1-gcp"
)


# connect to index
index = pinecone.Index(index_name)

def concatQuestions(last_few_questions):
    o = ""
    MAX_Q = len(last_few_questions)
    for i in range(0,MAX_Q):
        o = o + last_few_questions[i] + " "
    return(o)
    
def get_embedding(text):
    EMBEDDING_MODEL = "text-embedding-ada-002"
    result = openai.Embedding.create(
      model=EMBEDDING_MODEL,
      input=text
    )
    return result["data"][0]["embedding"]


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print(sqlite3.version)
    except Error as e:
        print(e)
    
    return conn
    
def get_context_by_id(conn, row_id):
    cur = conn.cursor()
    cur.execute("SELECT context FROM contexts WHERE id=?", (row_id,))

    rows = cur.fetchall()

    return(rows[0][0])
    
def getContext(query):
    #load files
    conn = create_connection("<PATH>/pythonsqlite.db")
    query_embedding = get_embedding(query)
    res = index.query(query_embedding, top_k=2)
    best_match = int(res['matches'][0]['id'])
    second_best_match = int(res['matches'][1]['id'])
    
    best_context = get_context_by_id(conn, best_match)
    second_best_context = get_context_by_id(conn, second_best_match)
    
    #top_contexts = best_context + "   " + second_best_context
    top_contexts = best_context 
    
    return(top_contexts)


