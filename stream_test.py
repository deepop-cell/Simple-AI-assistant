from openai import OpenAI
from dotenv import load_dotenv
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
      messages=[{"role":"user" , "content":"Hey what is an API ?Explain in 100 words and no need to mention number of words"}],
      tools=TOOLS,
      stream=True
   )
full_response=""
for chunks in stream:
    peice=chunks.choices[0].delta.content
    if peice:
        print(peice , end="" , flush=True)
        full_response+=peice

print("\n Full Response")
print(full_response)
