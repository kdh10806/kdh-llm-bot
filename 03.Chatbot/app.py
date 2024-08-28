from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = api_key)

messages = [] #message를 담는 리스트

def make_prompt(user_input):
    res = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role" : "user", "content" : user_input},
        ]
    )
    
    return res.choices[0].message.content

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form['user_input'] #json input으로 구현
        bot_response = make_prompt(user_input)
        
        messages.append({"role" : "user", "text":user_input})
        messages.append({"role" : "bot", "text":bot_response})
    
    return render_template('index.html', messages=messages)
    
        # return bot_response
        # 대화 리셋 버튼

@app.route('/delete', methods=["GET"])
def delete():
    messages.clear()
    
    return render_template('index.html', messages=messages)
    

if __name__ == "__main__":
    app.run(debug = True)