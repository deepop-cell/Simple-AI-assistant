from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS ,  FUNCTION_NAME_TO_FUNCTION
import os 
import json
load_dotenv()#by default looks for env file.
client =OpenAI(
  #base url hmari wahi ollama wali hai  aur ollama ko koi bhi api key ki jarurat nahi hoti 
    #isliye we used api key=dummy key yaani kuch b daldo.
     base_url=os.getenv("base_url"),#ollama serve for running ollama.
     api_key=os.getenv("api_key")
)
# now this is a one way talk , we want to make it loop, if we run while true , it will again and again send the same message .
# so kya karien??
#we want baat cheet between user and llm.
# to isske liye , har baar user se input le lenge .. (to make interactive loop)..
messages=[]
messages.append(
    #this tells ai model how to behave . (defining the behaviour).
    {
    "role":"system",
    "content":"Act like a very humble agent and always answer within 20 words."#telling LLM how to behave .
    }
)
while True:
    user_input=input("\nDeep:")
    #EXIT
    #user_input.lower() converts it into lower case so that bye and BYE is treated same.
    if user_input.lower() in ["exit","quit","bye","goodbye"]:
        break
    messages.append(#storing the user input for further context.
        {
          "role":"user",
          "content": user_input
        }

    )
    # first call to LLM api to ask which tool we should use as per the user query,,
    response=client.chat.completions.create(
        model=os.getenv("model"),
        messages=messages,
        tools=TOOLS
    )
    msg = response.choices[0].message
    if msg.tool_calls : # llms tells us which tools and with what parameters we have to call.
        messages.append(msg)
        for tool_call in msg.tool_calls :
            func_name = tool_call.function.name 
            func_args= json.loads(tool_call.function.arguments or "{}") # ye jo hai ye json format mai deta hai json.loads usse dixtcorinoary mai convert kr deta hai.

            fn = FUNCTION_NAME_TO_FUNCTION[func_name]
            result = fn(**func_args) ## operator func args ko dictironary se compatible arguements mai convert kr deta hai .
            messages.append({# after we have called the functions as told by LLm , now we will send the result of fn calls againt to LLM so it can make it in a good presenatble way .
                "role":"tool",
                "tool_id":tool_call.id,
                "content":str(result)# stores the result from function call. 
            })
             #2nd call to LLM API . 
        response=client.chat.completions.create(
         model=os.getenv("model"),
         messages=messages
         )
        msg=response.choices[0].message  

        messages.append({
            "role":"assistant",
            "content":msg.content
        })
        print("Assistant:" + msg.content)
    messages.append(#storint the llms response for chat history
        {
        "role":"assistant",#marking kiska response tha ye.
        "content": response.choices[0].message.content
        }
    )
    #todays topic is role "system".
    #the extra prompt to give personality to the agent...
    #instruction to llm to how to behave..
    #written by developer.
    print("LLM RESPONSE")
    #print( response)#ye poora python object fromat mai response deta hai .
    print("Asistant:"+response.choices[0].message.content)#this prints the response from the llm model
    #ollama-->json mai bhejta hai 
    print(response.choices[0].message.role)
    #but hum openai ka api use kr rhe hai to wo Python object mai bhejta hai (ChatCompletion).
    
