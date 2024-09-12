from flask import Flask, request, render_template, session
from dotenv import load_dotenv
import os
from openai import OpenAI
from utils import *

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

messages = []  # 채팅 내역을 저장하는 리스트
faq_data = []

# 앱이 시작되기 전에 FAQ 데이터를 한 번만 가져오는 함수
def initialize_faq_data():
    global faq_data
    faq_data = fetch_all_faqs()
    if not faq_data:
        raise Exception("FAQ 데이터를 불러오는 데 실패했습니다.")

@app.route('/', methods=["GET", "POST"])
def index():
    bot_response = ""
    
    # 'messages' 리스트가 비어있으면 기본 환영 메시지를 추가
    if not messages:
        messages.append({
            'role': 'assistant',
            'content': '안녕하세요! CS봇입니다. 문의하실 내용을 말씀해주시면 FAQ에서 찾아드릴께요!'
        })

    # 사용자가 대화를 시작함
    if request.method == 'POST':
        user_input = request.form['user_input']
        
        # 사용자 메시지를 먼저 추가
        messages.append({'role': 'user', 'content': user_input})
        
        # GPT 모델에 FAQ 데이터를 함께 전달하여 답변 생성(content 조정))
        conversation = [
            {"role": "system", "content": "FAQ의 JSON파일에 있는 내용만 답변해줘. 유저의 입력을 바탕으로 FAQ의 title을 탐색해서 관련있는 FAQ를 모두 찾아줘. 문의 내용이 FAQ의 JSON 데이터에 없으면 고객센터로 문의바랍니다라는 말로 대응해줘. 찾은 FAQ를 순번과 제목으로 보여주고 사용자가 보고싶은 FAQ를 순번으로 선택하면 선택한 FAQ에 대한 content를 보여주도록 해. 이전에 했던 대답은 다음 대답에 포함되지 않도록 해."}
        ]
        conversation.extend([{"role": msg['role'], "content": msg['content']} for msg in messages])
        
        bot_response = make_prompt_with_summary(conversation, faq_data)

        # 만약 FAQ 데이터에서 적절한 답변이 없으면 기본 답변을 제공
        if not bot_response or "고객센터로 연락" in bot_response:
            bot_response = "FAQ에서 해당 정보를 찾을 수 없습니다. 고객센터로 연락주세요."

        messages.append({'role': 'assistant', 'content': bot_response})

    # # 각 메시지의 URL을 링크로 변환
    # for message in messages:
    #     message['content'] = convert_urls_to_links(message['content'])

    return render_template('index.html', messages=messages)

if __name__ == "__main__":
    initialize_faq_data()
    app.run(debug=True)
