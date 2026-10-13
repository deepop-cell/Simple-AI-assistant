from openai import OpenAI
from dotenv import load_dotenv
import os 
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
while True:
    user_input=input("\nDeep:")
    #EXIT
    #user_input.lower() converts it into lower case so that bye and BYE os treated same.
    if user_input.lower() in ["exit","quit","bye","goodbye"]:
        break

    response=client.chat.completions.create(
        model=os.getenv("model"),
        messages=[
            {
                "role":"user",#helps to identify the speaker.
                "content":user_input#kya keh rha hai,
            }
        ]
    )
    print("LLM RESPONSE")
    #print( response)#ye poora python object fromat mai response deta hai .
    print("Asistant:"+response.choices[0].message.content)#this prints the response from the llm model
    #ollama-->json mai bhejta hai 
    print(response.choices[0].message.role)
    #but hum openai ka api use kr rhe hai to wo Python object mai bhejta hai (ChatCompletion).