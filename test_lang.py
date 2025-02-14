import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage


# 환경 변수 로드
load_dotenv()

# .env에서 API 키 가져오기
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini 모델 초기화 (API 키 적용)
model = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GEMINI_API_KEY,  # API 키 전달
    convert_system_message_to_human=True,  # 시스템 메시지를 사용자 메시지로 변환
    temperature = 0.7, #창의성 : 0.0~1.0 으로 높을 수록 창의적
    top_k = 50, #상위 k 개 단어 중에서 선택 
    top_p = 1, #80% 확률 이하의 단어는 제외 (1.0이면 모든 단어를 고려)
    max_output_tokens = 200, #최대 토큰 수 설정
)

# 메시지 설정
messages = [
    SystemMessage(content="You are an artificial intelligence that makes very emotional assessments."),  # 역할 및 성격 설정
    HumanMessage(content="Explain Van Gogh's paintings as long as possible")  # 사용자 질문
]

# 모델 응답 생성
response = model.invoke(messages)

# 응답 출력
print(response.content)
