import re
from openai import OpenAI
from sqlalchemy import text
import os
import requests

#OpenAI 클라이언트 설정
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# FAQ 리스트 가져오기 (GET 요청)
def fetch_all_faqs():
    faq_url = 'http://localhost:8080/cs/faq/allApi'
    try:
        # print(f"Sending GET request to: {faq_url}")  # 요청 URL을 확인하기 위한 로그
        response = requests.get(faq_url)  # GET 요청을 명확히 사용
        # print(f"Response status code: {response.status_code}")  # 응답 상태 코드 확인
        response.raise_for_status()  # 요청 오류가 있으면 예외 발생
        if response.status_code == 200:
            faq_data = response.json()
            # print("FAQ 데이터:", faq_data)  # 응답 데이터 로깅
            if faq_data:  # 데이터가 비어있지 않은지 확인
                return faq_data
            else:
                raise Exception("FAQ 데이터가 비어 있습니다.")
        else:
            raise Exception(f"FAQ 데이터를 불러오는 데 실패했습니다. 상태 코드: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"FAQ 데이터를 가져오는 중 오류가 발생했습니다: {e}")

# GPT 모델을 사용하여 FAQ 데이터를 참고해 답변 생성
def make_prompt(conversation, faq_data):
    # FAQ 데이터를 prompt에 추가
    faq_text = "\n".join([f"{faq['faq_title']}: {faq['faq_content']}" for faq in faq_data])
    
    # FAQ 데이터를 conversation에 추가
    conversation.append({
        "role": "system",
        "content": "Here are the available FAQs:\n" + faq_text
    })
    
    # GPT 모델에 요청
    res = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=conversation,
        max_tokens=150,
        temperature=0.7,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.6
    )
    
    # GPT의 응답 반환
    return res.choices[0].message.content

#Url을 link 로 변환
def convert_urls_to_links(text):
    url_pattern = r'(http[s]?://\S+)'
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)