import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from db_module import MongoDBConnection

class GeminiAPI:
    def __init__(self, api_key: str, db_connection: MongoDBConnection = None):
        """
        Gemini API 클라이언트 초기화 및 선택적으로 MongoDB 연결.
        
        :param api_key: Google Gemini API 키
        :param db_connection: db_module.py의 MongoDBConnection 인스턴스 (선택 사항)
        """
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.role = ""   # 기본 시스템 역할 (없으면 빈 문자열)
        
        # 전달받은 db_connection을 활용 (없으면 None)
        self.db_connection = db_connection
        self.db = self.db_connection.db if self.db_connection else None

    def set_role(self, role_text: str):
        """
        시스템 역할을 설정하여 모든 프롬프트에 선행하는 지침으로 사용.
        
        :param role_text: 시스템 역할 또는 지침 텍스트
        """
        self.role = role_text
        print("시스템 역할 설정됨.")

    def retrieve_context(self, query: str, collection_name: str = "documents", limit: int = 3) -> str:
        """
        RAG를 위한 문서 검색. MongoDB에서 관련 문서를 검색하여 컨텍스트로 반환.
        
        :param query: 사용자 쿼리 또는 프롬프트
        :param collection_name: 검색할 컬렉션 이름 (기본값: 'documents')
        :param limit: 반환할 문서 수 제한 (기본값: 3)
        :return: 검색된 문서들의 내용을 줄바꿈 문자로 연결한 문자열
        """
        if self.db is None:
            print("❌ MongoDB 연결이 없습니다. 컨텍스트를 검색할 수 없습니다.")
            return ""
        try:
            # 'content' 필드에 text index가 있다고 가정합니다.
            results = self.db[collection_name].find({"$text": {"$search": query}}).limit(limit)
            context = "\n".join([doc.get("content", "") for doc in results])
            return context
        except Exception as e:
            print(f"❌ 문서 검색 실패: {e}")
            return ""
    
    def compose_prompt(self, user_prompt: str) -> str:
        """
        시스템 역할, 검색된 컨텍스트, 그리고 사용자 프롬프트를 결합하여 최종 프롬프트를 구성.
        
        :param user_prompt: 사용자 입력 프롬프트
        :return: 최종 구성된 프롬프트 텍스트
        """
        prompt_parts = []
        if self.role:
            prompt_parts.append(f"System: {self.role}")
        # RAG: 검색된 컨텍스트 추가
        context = self.retrieve_context(user_prompt)
        if context:
            prompt_parts.append(f"Context: {context}")
        prompt_parts.append(f"User: {user_prompt}")
        full_prompt = "\n".join(prompt_parts)
        return full_prompt

    def generate_text(self, prompt: str, max_tokens: int = 200) -> str:
        """
        Gemini 모델을 사용하여 텍스트를 생성 (단순 프롬프트 사용).
        
        :param prompt: 입력 프롬프트
        :param max_tokens: 생성할 최대 토큰 수
        :return: 생성된 텍스트
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"max_output_tokens": max_tokens}
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_text_with_rag(self, user_prompt: str, max_tokens: int = 200) -> str:
        """
        RAG 기반 텍스트 생성: 시스템 역할과 검색된 컨텍스트를 포함한 프롬프트로 텍스트 생성.
        
        :param user_prompt: 사용자 입력 프롬프트
        :param max_tokens: 생성할 최대 토큰 수
        :return: 생성된 텍스트
        """
        full_prompt = self.compose_prompt(user_prompt)
        print("최종 프롬프트:\n", full_prompt)  # 디버그용 출력
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={"max_output_tokens": max_tokens}
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def insert_prompt(self, user_prompt: str, collection_name: str = "prompts"):
        """
        사용자 프롬프트를 MongoDB에 저장.
        
        :param user_prompt: 사용자 입력 프롬프트
        :param collection_name: 저장할 컬렉션 이름 (기본값: 'prompts')
        """
        if self.db is None:
            print("❌ MongoDB 연결이 없습니다. 프롬프트를 저장할 수 없습니다.")
            return
        try:
            data = {
                "prompt": user_prompt,
                "timestamp": datetime.now()
            }
            result = self.db[collection_name].insert_one(data)
            print(f"✅ 프롬프트 저장 성공 (문서 ID: {result.inserted_id})")
        except Exception as e:
            print(f"❌ 프롬프트 저장 실패: {e}")

    def save_response_to_db(self, collection_name: str, prompt: str, response: str):
        """
        Gemini API의 응답과 프롬프트, 그리고 현재 시간을 MongoDB에 저장.
        
        :param collection_name: 저장할 컬렉션 이름
        :param prompt: 사용자 입력 프롬프트 (시스템 역할, 컨텍스트 포함 가능)
        :param response: Gemini의 응답 텍스트
        """
        if self.db is None:
            print("❌ MongoDB 연결이 없습니다. 응답을 저장할 수 없습니다.")
            return
        try:
            data = {
                "prompt": prompt,
                "response": response,
                "timestamp": datetime.now()
            }
            result = self.db[collection_name].insert_one(data)
            print(f"✅ 데이터 저장 성공 (문서 ID: {result.inserted_id})")
        except Exception as e:
            print(f"❌ 데이터 저장 실패: {e}")
    
    def close_connection(self):
        """
        Gemini API 연결 해제 및 MongoDB 연결 종료 (있을 경우).
        """
        genai.configure(api_key=None)
        if self.db_connection:
            self.db_connection.close_connection()
        print("Gemini API 연결이 해제되었습니다.")


# === 적용 예시 ===

if __name__ == "__main__":
    load_dotenv()  # .env 파일 로드
    API_KEY = os.getenv("GEMINI_API_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME") or "gemini_db"

    if not API_KEY:
        raise ValueError("GEMINI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

    # db_module.py의 MongoDBConnection을 사용하여 DB 연결 생성
    db_connection = MongoDBConnection(MONGO_URI, DB_NAME)
    
    # GeminiAPI 생성 시, db_connection 인스턴스를 전달합니다.
    gemini = GeminiAPI(API_KEY, db_connection=db_connection)
    
    # 1. 시스템 역할 설정
    gemini.set_role("당신은 판사로 찬반 토론을 진행합니다.")
    
    # 2. 사용자 프롬프트 예시
    user_prompt = "토론 주제에 대해서 간략하게 설명해줘."
    
    # 3. 사용자 프롬프트를 DB에 저장 (분석 또는 추후 검색을 위해)
    gemini.insert_prompt(user_prompt)
    
    # 4. RAG 기반으로 최종 프롬프트를 구성하여 응답 생성
    response_text = gemini.generate_text_with_rag(user_prompt)
    print("판사:\n", response_text)
    
    # 5. 생성된 응답을 DB에 저장
    gemini.save_response_to_db("responses", user_prompt, response_text)
    
    # 6. Gemini API 및 MongoDB 연결 종료
    gemini.close_connection()
