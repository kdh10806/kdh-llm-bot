import requests
from bs4 import BeautifulSoup

# Step 1: 페이지 요청 및 BeautifulSoup 객체 생성
url = "https://www.musinsa.com/app/cs/faq/000"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}
response = requests.get(url, headers=headers)
response.raise_for_status()  # 요청이 성공했는지 확인
soup = BeautifulSoup(response.text, 'html.parser')

# Step 2 이후는 이전에 작성한 것과 동일합니다.

# Step 2: 카테고리, 제목, 내용 크롤링
faq_list = []

# FAQ 항목 찾기
faqs = soup.find_all('li', class_='faq-list__item')

for faq in faqs:
    # 카테고리, 제목, 내용 찾기
    category = faq.find('em', class_='faq-list__category').get_text(strip=True)
    title = faq.find('p', class_='faq-list__question').get_text(strip=True)
    content = faq.find('div', class_='faq-list__contents').get_text(strip=True)
    
    # 리스트에 추가
    faq_list.append((category, title, content))

# Step 3: SQL INSERT 문 생성 및 파일에 저장
with open('faq_insert_statements.txt', 'w', encoding='utf-8') as file:
    for category, title, content in faq_list:
        # 따옴표 이스케이프 처리
        category_escaped = category.replace("'", "''")
        title_escaped = title.replace("'", "''")
        content_escaped = content.replace("'", "''")
        
        # SQL 문 생성
        if category_escaped == '탈퇴/기타':
            category_escaped = 29
        if category_escaped == '로그인/정보':
            category_escaped = 30
        if category_escaped == '가입/인증':
            category_escaped = 31
    
  
        sql = f"INSERT INTO testingdb.FAQ (faq_category_code, faq_subcategory_id, faq_title, faq_content, writer, is_post) VALUES ('30006', {category_escaped}, '{title_escaped}', '{content_escaped}', 'kdh10806', 'Y');"
        
        # SQL 문을 파일에 저장
        file.write(sql + '\n')

print("SQL 문이 'faq_insert_statements.txt' 파일에 저장되었습니다.")
