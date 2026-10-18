from datetime import datetime
import requests
def get_current_time():
    return datetime.now().strftime("%Y-%m%d %H:%M:%S")

def get_city_weather(city):
    url=f"https://wttr.in/{city}?format=3"
    resp=requests.get(url,timeout=10)
    return resp.text
# LLMs actual math calculate nahi karte, wo bas data ke basis par agla word guess (predict) karte hain.
# Bade numbers me wo hallucinate (galat answer) kar dete hain kyunki unhe numbers ki mathematical value nahi pata hoti, wo bas unhe "tokens" (text chunks) ki tarah dekhte hain.
# Isliye exact aur 100% sahi result ke liye hum ye external Python function as a tool use karte hain, 
# taaki LLM bas intent samjhe aur actual math Python handle kare.
def calculate(num1,num2,operation):
    if operation=="add":
        return num1+num2
    elif operation=="subtract":
        return num1-num2
    elif operation=="multiply":
        return num1 * num2
    elif operation=="divide":
        if num2==0:
            return "Error:Cannot divide by Zero"
        return num1/num2
    else:
        return "Error:Unknown Operation"

def get_random_joke():
    #*** Koi bhi random sa joke maar dega .
    url="https://official-joke-api.appspot.com/random_joke"
    response=requests.get(url,timeout=10)
    return response.text
#TOOLS= [{},{},{}...]
TOOLS =[
    {
        "type" : "function",
        "function" : {
            "name" : "get_current_time",
            "description" : "Returns the current date and time as a formatted string",
            "parameters" : {
                "type" : "object",
                "properties":{#yaha pe parameters dalte ahai 
                }
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_city_weather",
            "description":"This tool returns the live weather of a given city.",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"city to get the weather for."
                    }
                }
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"calculate",
            "description":"A caclulator tool to perform exact math operations",
            "parameters":{
                "type":"object",
                "properties":{
                    "num1":{
                        "type":"number",
                        "description":"the first number"
                    },
                    "num2":{
                        "type":"number",
                        "description":"the second number"
                    },
                    "operation":{
                        "type":"string",
                        "enum":["add","subtract","multiply","divide"],
                        "description":"the math operation required to perform for the query"
                    }
                }
            }
        }
    },{
        "type":"function",
        "function":{
            "name":"get_random_joke",
            "description":"Gives a random joke to tell to the user",
            "parameters":{
                "type":"object",
                "properties":{}
            }
        }
    }
]
FUNCTION_NAME_TO_FUNCTION={
    "get_current_time" : get_current_time,
    "get_city_weather" : get_city_weather,
    "calculate" : calculate,
    "get_random_joke" : get_random_joke
}

