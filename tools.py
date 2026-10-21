from datetime import datetime
import requests
import webbrowser
import platform# this asks computer about its operating system(win or mac)
import shutil# this asks 
from Utilities.utilities import log
import time 
import threading
import json
def set_timer(hours):
    #see python works on only one thread (manlo worker )
    #maanlo ek restraunt hai waha pe sirf ek hee cook hai 
    # to ab agar uisko 60 min kaa kaam de doge to baaki ke kaam ruk jaenge 
    #threading se hum us kaam ko ek alag fn maoi likhke ek new worker banate hai 
    # new worker is created using threading.Thread() and iske andar target = assign krke isko kaam dete hai 
    # so now ek new extra worker hai jo backrgound mai timer wala kaam kr rha hota hai .
    def background_timer():#ye job description hai ki ye kaam lrna hai 
        seconds = hours * 3600
        time.sleep(seconds)
         # Only the background thread sleeps(ye is fn background_timer ko rok ke rkhega )
         #iske neeche ka part hours hour ke baad print hoga .
        print(f"\n\033[92mAssistant:  Beeeeep! Your timer for {hours} hours is up!\033[0m")
        print("\033[94mDeep:\033[0m ", end="", flush=True)

    timer_thread = threading.Thread(target=background_timer)#threading.Thread creates a new bakcground worker so the code still runs instead of stopping for hour hours.
    timer_thread.start()#target=background_timer this is way to assign the worker a task
    #timer_thread.start() makes the worker start the task 
    return f"Background timer successfully set for {hours} hours"

def get_current_time():
    return datetime.now().strftime("%Y-%m%d %H:%M:%S")

def get_city_weather(city):
    url=f"https://wttr.in/{city}?format=3"
    resp=requests.get(url,timeout=10)
    resp.raise_for_status()# This will raise HTTPError if something goes wrong with the req ( 4XX or 5XX means error ) 
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


def get_current_location():
    return "Kharagpur"



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
            },
            "required" : ["city"]#this tells the model that this parameter is mandatory for the function call.
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
            },
            "required":["num1","num2","operation"]
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
    },
    {
        "type":"function",
        "function":{
            "name":"get_current_location",
            "description":"gives the user's current location. use this when the user asks for my location , my city or my area when not specified any city ",
            "parameters":{
                "type": "object",
                "properties":{}
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"set_timer",
            "description":"sets a timer in the background when the user asks ",
            "parameters":{
                "type":"object",
                "properties":{
                    "hours":{
                        "type":"number",
                        "description":"amount of hours the user says to put the timer for "
                    }
                },
                "required":["hours"]
            }
        }
    }
]
FUNCTION_NAME_TO_FUNCTION={# this is basically a map of string(function name ) to  function.
    "get_current_time" : get_current_time,
    "get_city_weather" : get_city_weather,
    "calculate" : calculate,
    "get_random_joke" : get_random_joke,
    "open_website" : open_website,
    "get_system_info" : get_system_info,
    "get_current_location" : get_current_location,
    "set_timer" : set_timer

}
def run_tools(tool_call):
        func_name = tool_call.function.name
        func_args={}
        
        print(f"Agent is running tool: {func_name}...") 
        try:
            func_args= json.loads(tool_call.function.arguments or "{}") # ye jo hai ye json format mai deta hai json.loads usse dixtcorinoary mai convert kr deta hai.
            log(f" {func_name}({func_args})")
            fn = FUNCTION_NAME_TO_FUNCTION[func_name]
            #llm ne mujhe args is form ami diye hai eg "city" : "Kharagpur" (Ye dictionary wala form hai ).
            #but to pass in a fucnction we need it in form  of city=Kharagpur . ** does this 
            result = fn(**func_args) ## operator func args ko dictironary se compatible arguements mai convert kr deta hai .
        # originally fn args is in this form say city hai :->   "city":"KGP" this is dictionary form.
        # but fn mai humein ciyt=kgp ke form mai dalna padega . **converts dictrionary into this compatable format.
        except Exception as e:
            result=f"Error while running {func_name} : {e}"

        log(f"  ->>{result}")
        return result


