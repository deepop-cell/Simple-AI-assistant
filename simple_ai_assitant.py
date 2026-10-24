from openai import OpenAI
from dotenv import load_dotenv
from types import SimpleNamespace
from tools import TOOLS ,  FUNCTION_NAME_TO_FUNCTION,run_tools
from Utilities.utilities import log 
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
    "content":"You are a highly technical and precise AI assistant. You have access to external tools, but you also have vast general knowledge. ONLY use tools if the user's query specifically requires them (like fetching current data). For general knowledge questions, answer directly using your internal knowledge."#telling LLM how to behave .
    }
)


def build_tool_calls_payload(tool_calls):
    #it converts the collected tool calls into dictionary format that api expects insidde the assitant message
    payload=[]
    for tool_call in tool_calls:
        tool_call_dict={
            "id":tool_call.id,
            "type":"function",
            "function":{
                "name":tool_call.function.name,
                "arguments":tool_call.function.arguments
            },
        }
        payload.append(tool_call_dict)
    return payload

def stream_chat(history):# ye function streaming krne ke liye use kr rhe hai .
    stream=client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=history,
        tools=TOOLS,
        stream=True
    )
    full_response=""
    calls={}
    label_printed=False
    try:
        for chunks in stream:#streaming chal rha hai...
            if not chunks.choices:
                continue
            delta=chunks.choices[0].delta
            #Content streaming (Do we have message from LLm to print (STream)).
            if delta.content:
                if not label_printed:
                    print("ASSISTANT: " , end="",flush=True)
                    label_printed=True
                print(delta.content,end="",flush=True)
                full_response+=delta.content

            #check for tool calls and if present then accumulate them.
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    obj=calls.setdefault(tc.index , SimpleNamespace(id=None , function=SimpleNamespace(name="",arguments="")))
                    if tc.id:
                        obj.id=tc.id
                    if tc.function and tc.function.name:
                        obj.function.name +=tc.function.name
                    if tc.function and tc.function.arguments:
                        obj.function.arguments+=tc.function.arguments
    except KeyboardInterrupt:
        print("\n{stopped by You}")# to handle the case when the user does ctrl+c while the stream is running to handle it like chat gpt when we pause the chat stream 
        calls={}#nullify the calls
    if label_printed:
            print() # Move to the new line after assistants reponse.
    calls_list=[]
    for key in sorted(calls):
         calls_list.append(calls[key])

    return full_response,calls_list
        
#chat loop starts from here.
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

   #chain tool calling . 
    for step in range(MAX_STEPS) : # llms tells us which tools and with what parameters we have to call.(Lopping in while for chain tool calling)
        full_response,tool_calls=stream_chat(messages)

        #msg = response.choices[0].message 

        if not tool_calls:# no tool required now (LLM ne bol dia ki ab aur koi tool nahi  chaiye )
            break

        log(f"Step {step+1}:model requested {len(tool_calls)} tool call(s)")

        messages.append(
            {
                "role":"assistant",
                "content":full_response,
                "tool_calls":build_tool_calls_payload(tool_calls)
            }
        )#save the tool call

        for tool_call in tool_calls :#looping over the tools 
            result=run_tools(tool_call)

            messages.append({# after we have called the functions as told by LLm , now we will send the result of fn calls againt to LLM so it can make it in a good presenatble way .
                "role":"tool",
                "tool_call_id":tool_call.id,
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



    # print()"Assistant:"+msg.content or "")# or means if msg.content is None then append empty string (Warna error aa jaega string + None nahi kr skte )
    # #todays topic is role "system".
    # #the extra prompt to give personality to the agent...
    # #instruction to llm to how to behave..
    # #written by developer.
   
