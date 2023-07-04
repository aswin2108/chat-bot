from flask import Flask, request, render_template
import requests

from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_message = request.args.get('msg')
    if user_message in ['can you help me?', 'help me', 'help', 'sad', 'i am sad']:
        response = "Hey, chill out buddy, tell me what the problem is!"
    elif user_message in ['what is your name', 'what is ur name']:
        response = "I dont have a name, but I am your buddy...!"
    else:
        api_key = os.getenv("API_KEY")
        model="text-ada-001"
        response=generate_response_gpt3(user_message, model, api_key)
    return response

def generate_response_gpt3(user_message, model, api_key):
    prompt=(f"User: {user_message}\n"
            f"ChatBot:")
    response=requests.post(
        "https://api.openai.com/v1/engines/text-ada-001/completions",
        headers={"Authorization": f"Bearer {api_key}"},
                 json={
                     "prompt": prompt,
                     "max_tokens":200,
                     "temperature": 0.7,
                 },
    ).json()
    return response['choices'][0]['text'].strip()[len(prompt):]

if __name__=="__main__":
    app.run()