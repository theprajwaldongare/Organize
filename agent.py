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


def apiCall(prompt:str):
    response = client.chat.completions.parse(
        model="gemini-3.5-flash-lite",
        messages=[
        { "role": "user", "content": prompt}
    ]
    )

    result = response.choices[0].message.content
    
    return result

print(apiCall("hello!"))
