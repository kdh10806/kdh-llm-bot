# kdh-llm-bot
LLM chatbot to use Crawling

## 1. 프로젝트 세팅
- VSC
- Github

## 2. 프로젝트 구성
- 가상환경 설정 => ex) Docker Container 개념(공간을 분리해 따로 관리하겠다.)
- 로컬과 호스트 작업환경을 일치시키기 위해
- venv모듈 사용 (터미널에서 python3.10 -m venv .venv)
- source .venv/bin/activate

## 3. 프로젝트
### 3.1 Ollama 모델 + CrewAI
(1) Ollama 모델 다운
(2) Ollama 통해서 llm 모델 다운로드 - phi3:3.8b, 시간될때 llama3.1
(3) CrewAI 설치
- 언어 모델의 API 관리를 편리하게 도와주는 라이브러리
- 모델(sdk) : 클로드, 제미나이, GPT 3.5, GPT 4o => import OpenAI // 언어마다 SDK를 다운받아야한다.
   => CrewAI, LangChain이 이미 다 SDK 구현을 해놓음
   => LangChain 대신 CrewAI하는 이유 가볍고 learningCurb 낮음
pip install crewai crewai-tools
pip install langchain-ollama

(4) CrewAI 파일 작성

*REST Api -> 챗봇은 기술명세 기반으로 동작한다


### 3.2 Flask 사용 - 기본적인 챗봇
1. Flask 서버 세팅

2. 기본적인 라우팅 연습

3. 로컬 디비 세팅

4. 디비 데이터를 불러오는 REST API

5. LLM과 연동
