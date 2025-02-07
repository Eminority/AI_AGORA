import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiAPI:
    def __init__(self, api_key: str):
        """
        Google Gemini API 호출을 위한 초기화
        :param api_key: Google Gemini API 키
        """
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_text(self, prompt: str, max_tokens: int = 200) -> str:
        """
        Gemini 모델을 사용하여 텍스트 생성
        :param prompt: 사용자 입력 프롬프트
        :param max_tokens: 생성할 최대 토큰 수
        :return: 모델의 응답 텍스트
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"max_output_tokens": max_tokens}  # 변경된 부분
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    load_dotenv()  # .env 파일 로드
    API_KEY = os.getenv("GEMINI_API_KEY")  # 환경 변수에서 API 키 로드
    
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in the .env file")
    
    gemini = GeminiAPI(API_KEY)
    
    prompt_text = "Explain the concept of quantum entanglement in simple terms."
    response_text = gemini.generate_text(prompt_text)
    print("Gemini Response:", response_text)
