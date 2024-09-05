from flask import Flask, request, render_template, session
from dotenv import load_dotenv
import os
from openai import OpenAI
from utils import *
import re

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

messages = []  # 채팅 내역을 저장하는 리스트

def convert_urls_to_links(text):
    url_pattern = r'(http[s]?://\S+)'
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)

@app.route('/', methods=["GET", "POST"])
def index():
    bot_response = ""

    # 'messages' 리스트가 비어있으면 기본 환영 메시지를 추가
    if not messages:
        messages.append({
            'role': 'assistant',
            'content': '안녕하세요! CS봇입니다. 문의하실 내용을 말씀해주시면 FAQ에서 찾아드릴께요!'
        })

    if request.method == 'POST':
        user_input = request.form['user_input']
        
        # 사용자 메시지를 먼저 추가
        messages.append({'role': 'user', 'content': user_input})

        if '배송' in user_input or '예약' in user_input or '픽업' in user_input:
            bot_response = "배송과 관련된 FAQ를 보여드릴께요."
            messages.append({
                'role': 'assistant',
                
                'content': bot_response + '\n' + 'http://localhost:8080/cs/faq/list/30001'
            })
        elif '교환' in user_input or '취소' in user_input or '반품' in user_input or '환불' in user_input:
            bot_response = "교환/취소와 관련된 FAQ를 보여드릴께요."
            messages.append({
                'role': 'assistant',
                'content': bot_response + '\n' + 'http://localhost:8080/cs/faq/list/30002'
            })
        elif '혜택' in user_input or '고객센터' in user_input or '프로모션' in user_input or '이벤트' in user_input or 'PLUS' in user_input or \
             '서비스' in user_input or '테라스' in user_input or '웹' in user_input or '앱' in user_input or '후기' in user_input or \
             '전문관' in user_input or 'AS' in user_input or 'as' in user_input:
            bot_response = "서비스와 관련된 FAQ를 보여드릴께요."
            messages.append({
                'role': 'assistant',
                'content': bot_response + '\n' + 'http://localhost:8080/cs/faq/list/30003'
            })
        elif '결제수단' in user_input or '결제' in user_input or '수단' in user_input or '결제 수단' in user_input or '주문' in user_input or \
             '무신사페이' in user_input or '페이' in user_input:
            bot_response = "결제와 관련된 FAQ를 보여드릴께요."
            messages.append({
                'role': 'assistant',
                'content': bot_response + '\n' + 'http://localhost:8080/cs/faq/list/30004'
            })
        elif '상품확인' in user_input or '상품 확인' in user_input or '불량' in user_input or '하자' in user_input or '상품문의' in user_input or \
             '상품 문의' in user_input or '직매입' in user_input or '입점' in user_input:
            bot_response = "상품확인과 관련된 FAQ를 보여드릴께요."
            messages.append({
                'role': 'assistant',
                'content': bot_response + '\n' + 'http://localhost:8080/cs/faq/list/30005'
            })
        elif '탈퇴' in user_input or '로그인' in user_input or '회원가입' in user_input or '회원' in user_input or '가입' in user_input or \
             '회원 가입' in user_input or '인증' in user_input or '회원정보' in user_input or '회원 정보' in user_input:
            bot_response = "회원정보와 관련된 FAQ를 보여드릴께요."
            messages.append({
                'role': 'assistant',
                'content': bot_response + '\n' + 'http://localhost:8080/cs/faq/list/30006'
            })
        else:
            conversation = [
                {"role": "system", "content": "You are a very kind and helpful shopping mall C/S assistant."},
                {"role": "assistant", "content": "해당되는 FAQ가 없습니다. 어떻게 도와드릴까요?"}
            ]
            conversation.extend([{"role": msg['role'], "content": msg['content']} for msg in messages])
            conversation.append({"role": "user", "content": user_input})
            
            bot_response = make_prompt(conversation)

            messages.append({'role': 'assistant', 'content': bot_response})

    # 각 메시지의 URL을 링크로 변환
    for message in messages:
        message['content'] = convert_urls_to_links(message['content'])

    return render_template('index.html', messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
