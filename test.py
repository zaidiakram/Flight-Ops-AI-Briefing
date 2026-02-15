import os
from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="what is the capital of india"
)

print(response.text)