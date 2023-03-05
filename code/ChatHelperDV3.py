import openai
import os

def promptMaker(context,chat_history,next_question):
    p = """The following is a conversation with an AI assistant. The assistant will answer quetions ONLY based on the TEXT below and not on anything else.  If the assistant gets questions for which the answer is not in the TEXT below, it will say "I'm sorry, I cannot answer that since it is not in the information I was given.". 
    
    {context}
    
    {chat_history}
    Human:{next_question}
    AI:""".format(context=context,chat_history=chat_history,next_question=next_question)
    return(p)
    

def appendChatHistory(chat_history,last_question,last_response):
    c = """{chat_history}
    Human:{last_question}
    AI:{last_response}""".format(chat_history=chat_history,last_question=last_question,last_response=last_response)
    
    return(c)

def getResp(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    
    return(response["choices"][0]["text"])

def add_new_question(next_question, last_few_questions):
    MAX_Q = len(last_few_questions)
    for i in range(0,MAX_Q-1):
        last_few_questions[i] = last_few_questions[i+1]
    last_few_questions[MAX_Q-1] = next_question
    
    return(last_few_questions)

def chatRunner(context,chat_history,next_question,last_few_questions):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = promptMaker(context,chat_history,next_question)
    resp = getResp(prompt)
    chat_history = appendChatHistory(chat_history,next_question,resp)
    last_few_questions = add_new_question(next_question,last_few_questions)
    return(resp,chat_history,last_few_questions)
    
