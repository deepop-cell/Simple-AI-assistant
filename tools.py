from datetime import datetime
import requests
import webbrowser
import platform# this asks computer about its operating system(win or mac)
import shutil# this asks 
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

def open_website(url):
    #jo bhi website  bologe wo ye khol dega .
    if not url.startswith("http"):
        url = "https://" + url
    try:# try is the error handling block , agar error a gya to unknowingly loop end nahi krna hai .
        webbrowser.open(url)
        return f"Successfully opened {url} in your browser"
    except Exception as e:#catches the error in try block as e , and converts into string so LLM can tell what happened.
        return f"Error: Could not open browser. {str(e)}"

def get_system_info():
    #computer ka os aur storage space bata deta hai . 
    try: 
        total,used,free = shutil.disk_usage("/")# shutil.disk usage total , used aur free ke form mai dega . we can accesss direclty in py unlike cpp
        free_gb = round(free / (1024 ** 3), 2)
        total_gb = round(total / (1024 ** 3), 2)

        system_os = platform.system()# konsa hai win , mac etc etc 
        os_version = platform.release()# number
        return f"System:{system_os}, {os_version}, Free Storage:{free_gb}GB out of {total_gb}GB"
    except Exception as e:
        return f"Error getting system info: {str(e)}"# if catches any error 
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
    },
    {
        "type":"function",
        "function":{
            "name":"open_website",
            "description":"opens the website of the url given by user",
            "parameters":{
                "type":"object",
                "properties":{
                    "url":{
                        "type":"string",
                        "description":"url of the website user want's to open"
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_system_info",
            "description":"Gives the information about operating system and storage used and total storage of the users computer",
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
    "get_random_joke" : get_random_joke,
    "open_website" : open_website,
    "get_system_info" : get_system_info
}

