import os
def log(text):
    if os.getenv("DEBUG")=="True":
     print(f" \033[91m{text}\033[0m")
     #this is used to print the log things in different colour . 
     #\033- this thing tells the terminal that the upcoming text is a command 
     #[ indicates the starting of command 
     # 90 - code for grey colour , 91- code  for red colour
     #m marks that the command has ended 
     # but we need to make sure that this colour effect is only for certain text 
     # so jitne text ko colour krna hai usse baad ]033[0m add krdo . 0 means jo bhi commmand tha usse ab roke do 
