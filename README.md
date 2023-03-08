# Chatbot-using-GPT35-turbo

Chatbot using the OpenAI ChatGPT API, Pinecone and SQLLite.

I have a writeup explaining what I did here: https://medium.com/@venkat.ramrao/building-a-chatbot-using-a-local-knowledge-base-chatgpt-and-pinecone-d107745a472a

This is designed to answer questions based on a local knowledgebase of articles. I was testing out concepts around Vector databases and trying out Prompts to see how far I could push the model without resorting to fine-tuning.

SINGLE HOP Question Answering only at this time. Hoping to add in MULTI HOP QA in the future

PREREQUISITES:
You will need API Keys for OpenAI and Pinecone stored in environment variables - OPENAI_API_KEY and PINECONE_API_KEY

EXPLANATION OF CODE FILES

1) createIndex - This expects the knowledge base to be provided as a set of .txt files in a folder. It creates an embedding for each file using text-embedding-ada-002 and loads them into an index in Pinecone. It also stores the actual text in a local SQLLite database.
2) EmbeddingsHelper - Stores methods to retrieve context
3) main35T  &  ChatHelper35T - Implementation using gpt-3.5 turbo (ChatGPT API). You need to run main35T.py
4) mainDV3  &  ChatHelperDV3 - alternative implementation using davinci-003
