
import os
from debate.ai_module.gemini import GeminiAPI
import json
from dotenv import load_dotenv
import google.generativeai as genai
from db_module import MongoDBConnection
from vectorstore_module import VectorStoreHandler  # 벡터스토어 관련 모듈
from detect_persona import DetectPersona
from debate.ai_module.ai_factory import AI_Factory

if __name__ == "__main__":

    #MONGO_URI, DB_NAME 확인
    load_dotenv()  # .env 파일 로드

    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")

    for var_name, var_value in [("MONGO_URI", MONGO_URI),
                                ("DB_NAME", DB_NAME)]:
        if not var_value:
            raise ValueError(f"{var_name}가 .env파일에 설정되어있지 않습니다.")
     # MongoDB 연결 생성
    db_connection = MongoDBConnection(MONGO_URI, DB_NAME)

    # .env에 JSON형태로 저장된 API KEY를 dict 형태로 불러오기
    AI_API_KEY = json.loads(os.getenv("AI_API_KEY"))
    ai_factory = AI_Factory(AI_API_KEY)
    
    # ✅ DetectPersona 인스턴스 생성 (db_connection 전달)
    persona_detector = DetectPersona(db_connection=db_connection, AI_API_KEY=AI_API_KEY["GEMINI"])

    # 객체 이름 입력
    object_name = input("🔍 분석할 객체 이름을 입력하세요: ").strip()

    # 🔹 검색 및 성격 분석 모델 설정
    persona_detector.select_source_and_model()
    

    # 🔍 객체 성격 분석 실행 (DB 저장 포함)
    persona_detector.get_traits(object_name)

    # ✅ 터미널 출력 없이 DB에만 저장
    print("✅ 프로필이 DB에 저장되었습니다.")  # 🔹 확인 메시지만 출력

    # ✅ 연결 종료
    db_connection.close_connection()