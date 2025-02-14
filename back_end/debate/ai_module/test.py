import os
from dotenv import load_dotenv
from gemini import GeminiAPI  # 위에서 만든 GeminiAPI 클래스
import google.generativeai as genai

# 환경 변수 로드 (.env 파일에서 API 키 가져오기)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ 테스트할 Gemini 모델 목록
models = ["gemini-2.0-flash", "gemini-pro"]

# ✅ 비교할 질문 목록
test_questions = [
  
    "Guess who I am by giving me proper evidence."
]

# 모델별 테스트 수행
for model_name in models:
    print(f"\n🔹 Testing model: {model_name}")
    
    # Gemini 모델 초기화
    gemini = GeminiAPI(api_key=GEMINI_API_KEY)
    gemini.model = gemini.model = genai.GenerativeModel(model_name)  # 모델 변경
    
    for question in test_questions:
        print(f"\n🚀 **Prompt:** {question}")
        response = gemini.generate_text(question, max_tokens=100)
        print(f"✍️ **{model_name} Response:**\n{response}\n")
    
    # API 연결 해제
    gemini.close_connection()
