import openai
import sys
from gtts import gTTS
# Ensure UTF-8 output in Windows terminal
sys.stdout.reconfigure(encoding="utf-8")

openai.api_key = ""  # Replace with your actual key

# Function to parse and generate summary based on job description
def generate_information(name , language = "English"):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the model you prefer
        messages=[
            {"role": "system", "content": "You are entomologists , zoologists , ornithologists ."},
            {"role": "user", "content": f" Please give me the information about : {name} , in 100 words in points also only in language {language}."}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

