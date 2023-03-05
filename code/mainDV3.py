from EmbeddingsHelper import *
from ChatHelperDV3 import *

#=============INITIALIZE==================
chat_history = """Human: Hello, who are you?
AI: I am an AI created by OpenAI. How can I help you today?
Human:Hi, I am Bob
AI:Hi Bob! How can I help you?
Human:Did the US Sign the Paris Agreement?
AI:I'm sorry, I cannot answer that since it is not in the information I was given."""

context = '' #unique_contexts[0]

QUESTIONS_TO_SV = 2 #retains these main questions to find context

last_few_questions = {}
for i in range(0,QUESTIONS_TO_SV):
    last_few_questions[i] = ""

#========================================


#=============MAIN LOOP==================

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
    chat_history = c
    last_few_questions = l
    print("AI: " + r)
    print("===================")

#========================================
