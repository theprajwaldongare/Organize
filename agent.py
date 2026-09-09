from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel,Field
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

folderUrl = "FolderToOrganize"

def readFolderContent(folderUrl:str,relativePath: str = "",complete = []):

    if not os.path.exists(folderUrl):
        print("Folder path does not exists")
        return
    
    items = os.listdir(folderUrl)

    

    if len(items)==0: # for empty folder to show 
        print(f"{relativePath} [Empty Folder]")
        complete.append(f"{relativePath} [Empty Folder]")
        return
    
    for i in items:
        
        if i.startswith("."): # hidden files
            continue 
        currRelative = os.path.join(relativePath,i)
        fullPath = os.path.join(folderUrl,i)

        if os.path.isdir(fullPath):
            readFolderContent(fullPath,currRelative,complete=complete)
        else:
            print(currRelative) # only when its file .. it create empty folder problem .. we never know empty folder exists .. 
            complete.append(currRelative)

    return complete

allFolderFiles = readFolderContent(folderUrl)
print(allFolderFiles)

def apiCall(prompt:str):
    response = client.chat.completions.parse(
        model="gemini-3.5-flash-lite",
        messages=[
        { "role": "user", "content": prompt}
    ]
    )

    result = response.choices[0].message.content
    
    return result

# print(apiCall("hello!"))
