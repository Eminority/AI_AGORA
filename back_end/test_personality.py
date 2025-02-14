import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from pymongo import MongoClient

# ✅ 환경 변수 로드
load_dotenv()

# ✅ .env에서 MongoDB 및 Gemini API 정보 가져오기

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")




# ✅ 테스트할 인물 이름
character_name = input("🔍 테스트할 인물 이름을 입력하세요: ").strip()


# ✅ Gemini 모델 초기화
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,  # 창의성 조절
    top_k=40,  # 상위 40개 단어 중에서 선택
    max_output_tokens=200,  # 최대 생성 토큰 수
)

# ✅ Ollama 모델 초기화
ollama_model = ChatOllama(model="llama3.2")  # Ollama 로컬 모델 설정

personality = "Precise and reliable."
# ✅ 메시지 설정
messages = [
    SystemMessage(content=f" {personality}"),  # MongoDB에서 불러온 역할 & 성격 적용
    HumanMessage(content="What do you think about humanity?")  # 사용자 질문
]

# ✅ Gemini 응답 생성
gemini_response = gemini_model.invoke(messages)

# ✅ Ollama 응답 생성
ollama_response = ollama_model.invoke(messages)

# ✅ 결과 출력
print("\n🔹 **Gemini Response:**")
print(gemini_response.content)

print("\n🔹 **Ollama Response:**")
print(ollama_response.content)



