from crewai import Crew, Agent, Task
from langchain_ollama import ChatOllama
#from openai import OpenAI

#Ollama 모델 설정
llm = ChatOllama(
    model = 'phi3:3.8b',
    base_url = 'http://localhost:11434'
)

#서점 쇼핑몰
user_question = input('편하게 질문해주세요 : ')

book_agent = Agent(
    role="책 구매 어시스턴스",
    goal="고객이 어떤 상황인지 설명을 하면 해당 상황에 맞는 우리 서점에 있는 책을 추천해줍니다.",
    backstory="당신은 우리 서점의 모든 책 정보를 알고있으며, 사람들의 상황에 맞는 책을 소개하는 일에 전문적입니다.",
    llm=llm
)

recommend_book_task = Task(
    # description="고객의 상황에 맞는 최고의 추천 도서 제안하기",
    description=user_question,
    expected_output="고객의 상황에 맞는 5개의 도서를 추천해주고, 해당 도서를 추천한 간단한 이유를 알려주십시오.",
    agent=book_agent,
    output_file="recommend_book_task.md"
)

review_agent = Agent(
    role="책 리뷰 어시스턴스",
    goal="추천받은 책들의 도서에 대한 리뷰를 제공하고, 해당 도서에 대한 심도있는 평가를 제공합니다.",
    backstory="당신은 우리 서점의 모든 책 정보를 알고있으며, 추천받은 책에 대한 전문가 수준의 리뷰를 제공합니다.",
    llm=llm
)

book_review_task = Task(
    description="고객이 선택한 책에 대한 리뷰를 제공합니다.",
    expected_output="고객이 선택한 책에 대한 리뷰를 제공합니다.",
    agent=review_agent,
    output_file="review_task.md"
)

#agent와 task를 관리
crew = Crew(
    agents=[book_agent, review_agent],
    tasks=[recommend_book_task, book_review_task],
    verbose=True
)

result = crew.kickoff()

print(result)

#Task 답변 기반으로 Agent가 답변을 만들고 전달함
#RAG : 확장하는 기능 => pdf, db 데이터 조회 => 답변