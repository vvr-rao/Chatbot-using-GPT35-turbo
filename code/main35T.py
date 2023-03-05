from EmbeddingsHelper import *
from ChatHelper35T import *

#=============INITIALIZE==================
chat_history = [  {'role': 'system', 'content': """You are an AI Assistant with limited knowledge. Answer my question only on the information given. It the information is not there say "I'm sorry, I cannot answer that since it is not in the information I was given." """},
        {"role": "user", "content": "Hi, I am Bob"},
        {"role": "assistant", "content": "Hi Bob! How can I help you?"},
        {"role": "user", "content": "Did the US Sign the Paris Agreement?"},
        {"role": "assistant", "content": "I'm sorry, I cannot answer that since it is not in the information I was given."}]

QUESTIONS_TO_SV = 2 #retains these many questions to find context

last_few_questions = {}
for i in range(0,QUESTIONS_TO_SV):
    last_few_questions[i] = ""

#=========================================

#=============MAIN LOOP===================

while True:
    next_question = input('Human(enter q to quit):')
    if next_question == 'q':
        break
    
    context_searcher = concatQuestions(last_few_questions) + " " + next_question
    #print("Context Searcher =>> " + context_searcher)
    #use Pinecone to retrieve Context based on the past few questions
    context = getContext(context_searcher) 
    
    #print("===================")
    #print(context)
    #print("===================")
    r, c, l = chatRunner(context,chat_history,next_question,last_few_questions)
    #print("===================")
    chat_history = c
    last_few_questions = l
    #print(chat_history )
    print("AI: " + r)
    #print("===================")
    
    
#=========================================
