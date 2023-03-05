import openai
import os

def getResp(inp):
    resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            top_p=1,
            messages=inp      #this will be a list with the context and prior chat messages
        )
    
    return(resp["choices"][0]["message"]["content"])
    
def user_question_dict(txt):
    # create a dictionary to hold the question
    return({"role": "user", "content": txt})

def ai_answer_dict(txt):
    # create a dictionary to hold the answer
    return({"role": "assistant", "content": txt})
    
def append_to_chat_history(chat_history, new_row):
    # mintain chat history minus the context
    out_list = chat_history
    out_list.append(new_row)

    return(out_list)


def add_question_to_chat(chat_history, txt):
    # accept a question as text and append to the chat history
    q_dict = user_question_dict(txt)
    return(append_to_chat_history(chat_history, q_dict))

def add_answer_to_chat(chat_history, txt):
    # accept an answer as text and append to the chat history
    a_dict = ai_answer_dict(txt)
    return(append_to_chat_history(chat_history, a_dict))


def construct_input(context, chat_hist, question):
    '''
    construct an input for gpt-3.5 with the  chat history, the last question and 
    the context you want the AI to use for he answer
    '''
    out = []
    out.extend(chat_hist)
    
    #This has some Chain of Thought reasoning to help the AI know when to answer
    prompt = """You are an AI Assistant with limited knowledge. Answer my question only using the information given. It the information is not there say "I'm sorry, I cannot answer that since it is not in the information I was given.". 
    Knowledge cutoff: {context}
    
    QUESTION: {question}
    Check if the knowledge provided has the answer to my question. If it does, answer the question. If not say "I'm sorry, I cannot answer that since it is not in the information I was given."

    """.format(context=context, question=question)
    
    '''
    prompt = """You are an AI Assistant with limited knowledge. Answer my question only using the information given. It the information is not there say "I'm sorry, I cannot answer that since it is not in the information I was given.". 
    Knowledge cutoff: {context}
    
    QUESTION: {question}

    """.format(context=context, question=question)
    '''

    prompt_line = {'role': 'user', 'content': prompt}
    out.append(prompt_line)
    
    
    return(out)

def add_new_question(next_question, last_few_questions):
    MAX_Q = len(last_few_questions)
    for i in range(0,MAX_Q-1):
        last_few_questions[i] = last_few_questions[i+1]
    last_few_questions[MAX_Q-1] = next_question
    
    return(last_few_questions)
    
def chatRunner(context,chat_history,next_question,last_few_questions):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    inp = construct_input(context,chat_history,next_question)
    
    resp = getResp(inp)
    
    c = add_question_to_chat( chat_history, next_question)
    chat_history = c
    c = add_answer_to_chat( chat_history, resp)
    chat_history = c
    
    last_few_questions = add_new_question(next_question,last_few_questions)
    return(resp,chat_history,last_few_questions)




