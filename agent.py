from dotenv import load_dotenv
from datetime import datetime
from openai import OpenAI
import os
import json
import re

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/",
    timeout=120.0,
    max_retries=5
)

#C:\\Users\\
folderUrl = "FolderToOrganize"

def readFolderContent(folderUrl:str,relativePath: str = "",complete = []):

    if not os.path.exists(folderUrl):
        print("Folder path does not exists")
        return
    
    items = os.listdir(folderUrl)

    

    if len(items)==0: # for empty folder to show 
        # print(f"{relativePath} [Empty Folder]")
        complete.append(f"{relativePath} [Empty Folder]")
        return
    
    for i in items:
        
        if i.startswith("."): # hidden files
            continue 
        currRelative = os.path.join(relativePath,i).replace("\\","/")
        fullPath = os.path.join(folderUrl,i)

        if os.path.isdir(fullPath):
            readFolderContent(fullPath,currRelative,complete=complete)
        else:
            # print(currRelative) # only when its file .. it create empty folder problem .. we never know empty folder exists .. 
            complete.append(currRelative)

    return complete

SYSTEM_PROMPT = """
You are an automated file organization assistant.
I will provide a list of file paths.
Your job is to cluster them into logical folders based on their file types and names(e.g., put 'lectureNotes.txt' and 'lectureScreenshot.png' in a 'Lectures' folder).

Rules:

1. Use existing folders (like 'Wallpapers') if the file belongs there.
2. Create new logical folder names for the rest.
3. Do not change the actual file names, only the folder they belong in.
4. STRICTLY use forward slashes (/) for all directory separators. No backslashes (\\).

OUTPUT STRICTLY AS A JSON DICTIONARY where the key is the original file path, and the value is the new destination path. Do not include any other text or markdown."

Output Sample:

{
  "lectureNotes.txt": "Lectures/lectureNotes.txt",
  "lectureScreenshot.png": "Lectures/lectureScreenshot.png",
  "movie.mp4": "Movies/movie.mp4",
  "Wallpapers/City/paris.jpeg": "Wallpapers/City/paris.jpeg",
  "nature.jpg": "Wallpapers/nature.jpg"
}


"""


allFolderFiles = readFolderContent(folderUrl)
print("\n")
print("INPUT: ")
print(allFolderFiles)

def apiCall(prompt:list[str]):
    response = client.chat.completions.parse(
        model="gemini-3.5-flash-lite",
        messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": prompt}
    ]
    )

    result = response.choices[0].message.content
    
    return result

# print(str(allFolderFiles))
# print(allFolderFiles)

print("\n")
print("OUTPUT: ")

apiResult = apiCall(str(allFolderFiles))
print(apiResult)



def gemmaApiCall(prompt: list):
    response = client.chat.completions.create(
        model="gemma-4-31b-it",
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": str(prompt)}
        ]
    )

    raw = response.choices[0].message.content
    
    clean = re.sub(r'<thought>.*?</thought>', '', raw, flags=re.DOTALL)
    
    clean = clean.replace("```json", "").replace("```", "").strip()
    
    try:
        final_dict = json.loads(clean)
        return final_dict
    except json.JSONDecodeError:
        print("Invalid output by Gemma")
        return None

# plan = gemmaApiCall(allFolderFiles)
# print(plan)

# Moving files

try:
    userInp = input("Do you want to continue the plan?(YES/NO) it changes your folder structure: ")
    if userInp.lower() != "yes":
        exit()
    
    result = json.loads(apiResult)

    savedHistory = "history.json"

    if os.path.exists(savedHistory):
        with open(savedHistory,"r") as f:
            jsonDataHistory = json.load(f)
    else:
        jsonDataHistory={}

    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    session_data = {
        "session_time": timestamp,
        "moves": result
    }
    
    if folderUrl not in jsonDataHistory:
        jsonDataHistory[folderUrl]=[session_data]
    else:
        # append in already changed
        jsonDataHistory[folderUrl].append(session_data)
    
    with open(savedHistory,"w") as f:
        json.dump(jsonDataHistory,f,indent=4)
    # print(result)

    if result:
        for key in result:
            if key==result[key]:
                pass
            elif "[Empty Folder]" in key:
                pass
            else:
                # os.rename(key,result[key]) it wont create folder itself ...
                initalPath = os.path.join(folderUrl,key)
                destPath = os.path.join(folderUrl,result[key])

                destFolder = os.path.dirname(destPath)

                os.makedirs(destFolder,exist_ok=True)
                os.rename(initalPath,destPath)
                print(f"Moved: {key} -> {result[key]}")



except Exception as e:
    print("Error: ",e)

