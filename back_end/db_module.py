import os
from dotenv import load_dotenv
from pymongo import MongoClient
import google.generativeai as genai

# MongoDB 연결 및 데이터 저장 클래스
class MongoDBConnection:
    def __init__(self, uri: str, db_name: str):
        """
        MongoDB 연결을 위한 초기화.
        :param uri: MongoDB 연결 URI
        :param db_name: 사용할 데이터베이스 이름
        """
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            # 연결 테스트
            self.client.admin.command('ping')
            print("✅ DB Connection Succeeded")
        except Exception as e:
            print("❌ Connection failed:", e)


    def close_connection(self):
        """
        MongoDB 연결 종료
        """
        self.client.close()
        print("🔌 MongoDB 연결 해제됨")



"""
if __name__ == "__main__":
    # 환경 변수 로드
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not MONGO_URI or not DB_NAME or not GEMINI_API_KEY:
        raise ValueError("MONGO_URI, DB_NAME 또는 GEMINI_API_KEY가 .env 파일에 설정되지 않았습니다.")

    # MongoDB 연결 객체 생성
    db_connection = MongoDBConnection(MONGO_URI, DB_NAME)

    # 사용자로부터 프롬프트 입력 (예: 역할을 포함한 프롬프트)
    prompt_input = input("역할을 포함한 프롬프트를 입력하세요: ")
    
    # Gemini API를 호출하여 응답 생성
    gemini_response = get_gemini_response(prompt_input, GEMINI_API_KEY)
    print("Gemini Response:", gemini_response)
    
    # 결과를 MongoDB의 "conversations" 컬렉션에 저장 (프롬프트, 응답, 타임스탬프 포함)
    COLLECTION_NAME = "conversations"
    db_connection.save_response_to_db(COLLECTION_NAME, prompt_input, gemini_response)
    
    # MongoDB 연결 종료
    db_connection.close_connection()
    
"""