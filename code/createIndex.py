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

#Get/Create pinecone index
# check if index already exists (it shouldn't if this is first time)
if index_name not in pinecone.list_indexes():
    # if does not exist, create index
    pinecone.create_index(
        index_name,
        dimension=1536, #ada-002 embeding length
        metric='cosine',
        metadata_config={'indexed': ['id']}
    )

# connect to index
index = pinecone.Index(index_name)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_context(conn, context):


    sql = ''' INSERT INTO contexts(id, context)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, context)
    conn.commit()

    return cur.lastrowid
    

def get_context_by_id(conn, row_id):
    cur = conn.cursor()
    cur.execute("SELECT context FROM contexts WHERE id=?", (row_id,))

    rows = cur.fetchall()

    return(rows[0][0])


def get_embedding(text):
    EMBEDDING_MODEL = "text-embedding-ada-002"
    result = openai.Embedding.create(
      model=EMBEDDING_MODEL,
      input=text
    )
    return result["data"][0]["embedding"]

def load_and_make_embeddings(file_path):
    #create SQLLite connection and table
    conn = create_connection("/home/ec2-user/environment/Project-Chatbot/pythonsqlite.db")
    
    sql_create_contexts_table = """ CREATE TABLE IF NOT EXISTS contexts (
                                    id integer PRIMARY KEY,
                                    context text
                                ); """
 
    # create tables in SQLLite db
    if conn is not None:
        # create  table
        create_table(conn, sql_create_contexts_table)
        print("Table created.")
        
        
    #load files
    unique_contexts = []

    for dirname, _, filenames in os.walk(file_path):
        for filename in filenames:
            pth = os.path.join(dirname, filename)
            #print(pth)
            split_tup = os.path.splitext(filename)
            #print(split_tup[1])
            if split_tup[1] == '.txt':
                f = open(pth, "r")
                context = f.read()
                unique_contexts.append(context)
    

    
    #create embeddings for all the contexts and load into Pinecone
    tot_contexts = len(unique_contexts)
    upsert_list = []
    for i in tqdm(range (0,tot_contexts), total=tot_contexts, desc="status:"):
        key = i
        text = unique_contexts[i]
        embedding = get_embedding(unique_contexts[i])
        #insert_tup = (str(key), embedding, {"id":key, "text":unique_contexts[i] })
        #could not include text in te metadata: Maximum size is 10 KB
        insert_tup = (str(key), embedding)
        upsert_list.append(insert_tup)
    
    print("Inserting into index " + index_name)
    index.upsert(upsert_list)
    
    #convert the contexts to a dictionary and save them as well
    all_contexts = {}
    i = 0
    for c in unique_contexts:
        context_to_insert = (i,c)
        insert_context(conn, context_to_insert)
        i = i + 1
    
    print("Contexts Inserted: " + str(i))
    #save contexts



load_and_make_embeddings('<PATH TO ARTICLES>')
