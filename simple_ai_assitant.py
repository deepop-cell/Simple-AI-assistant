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
MAX_STEPS=5# max number of times we wanna run the tool call thing ( chain tool calling) .
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
    for step in range(MAX_STEPS) : # llms tells us which tools and with what parameters we have to call.(Lopping in while for chain tool calling)
        response=client.chat.completions.create(#pass the whole history of messages for context + tools.
        model=os.getenv("model"),
        messages=messages,
        tools=TOOLS
        )

        msg = response.choices[0].message 

        if not msg.tool_calls:# no tool required now (LLM ne bol dia ki ab aur koi tool nahi  chaiye )
            break

        messages.append(msg)#save the tool call

        for tool_call in msg.tool_calls :#looping over the tools 
            func_name = tool_call.function.name
            func_args={}
            
            print(f"Agent is running tool: {func_name}...") 
            try:
              func_args= json.loads(tool_call.function.arguments or "{}") # ye jo hai ye json format mai deta hai json.loads usse dixtcorinoary mai convert kr deta hai.
              fn = FUNCTION_NAME_TO_FUNCTION[func_name]
              result = fn(**func_args) ## operator func args ko dictironary se compatible arguements mai convert kr deta hai .
            # originally fn args is in this form say city hai :->   "city":"KGP" this is dictionary form.
            # but fn mai humein ciyt=kgp ke form mai dalna padega . **converts dictrionary into this compatable format.
            except Exception as e:
                result=f"Error while running {func_name} : {e}"


            messages.append({# after we have called the functions as told by LLm , now we will send the result of fn calls againt to LLM so it can make it in a good presenatble way .
                "role":"tool",
                "tool_id":tool_call.id,
                "content":str(result)# stores the result from function call. 
            })
    else:#in python else after for only hits when the for loop runs normally without breaking while running.
        #Ran out of steps (for loop completely exhausted).
        fallback="Sorry I could not finish it within the step limit"
        messages.append(
            {
                "role":"assistant",
                "content":fallback

            }
        )
        print("Assistant:" + fallback)
        continue#this is for the outer while loop.LLM was unable to tool call perfectly so it asks again for new input instead of  going down.

    messages.append(#storint the llms response for chat history
        {
        "role":"assistant",#marking kiska response tha ye.
        "content": msg.content
        }
    )

    print("Assistant:"+msg.content)
    #todays topic is role "system".
    #the extra prompt to give personality to the agent...
    #instruction to llm to how to behave..
    #written by developer.
   
