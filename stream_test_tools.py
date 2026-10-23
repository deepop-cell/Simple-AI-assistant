from openai import OpenAI
from dotenv import load_dotenv
from types import SimpleNamespace
from tools import TOOLS ,  FUNCTION_NAME_TO_FUNCTION,run_tools
from Utilities.utilities import log 
import os 
import json
load_dotenv()
client=OpenAI(
    base_url=os.getenv("base_url"),
    api_key=os.getenv("api_key")
)
stream=client.chat.completions.create(
      model=os.getenv("MODEL"),
      messages=[{"role":"user" , "content":"Hey what is the weather in kgp and weather in Pune?"}],
      tools=TOOLS,
      stream=True
   )
full_response=""
calls={}#dictironary storing key index to value that is tool call.
for chunks in stream:# stream gives us response as it is formed simulataneoulsy
    peice=chunks.choices[0].delta.content
    d=chunks.choices[0].delta
    for tc in (d.tool_calls or []):# check if there are any tool call(s) in this chunk
        obj=calls.setdefault(tc.index , SimpleNamespace(id=None , function=SimpleNamespace(name="",arguments="")))
        #set ddef checks for the current tc.index in map if it is there then return its pair ( that is object here )
        # so for current tools index we get the object 
        if tc.id:# id waise sirf first time aaati hai .
            obj.id=tc.id
        if tc.function and tc.function.name:# tc can have name of function and args in different pieces and in any order.
            obj.function.name +=tc.function.name
        if tc.function and  tc.function.arguments:
            obj.function.arguments +=tc.function.arguments

    # if d.tool_calls:
    #     # note that even tho we are using stream but its qwen model oroperoty that it will send info one tool call together only.
    #     # so this is aactually good , we dont need to cumulate different chunks for  a single tool call.
    #     print(d.tool_calls, end="",flush=True)
    if peice:
        print(peice , end="" , flush=True)
        full_response+=peice
call_lists=[]
for key in sorted(calls):
    call_lists.append(calls[key])
