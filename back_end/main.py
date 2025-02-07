from call_gemini_module import GeminiAPI
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from db_module import MongoDBConnection
from vectorstore_module import VectorStoreHandler  # 벡터스토어 관련 모듈 임포트
from debate.ai_module.ai_factory import AI_Factory
from debate.participants import ParticipantFactory 

if __name__ == "__main__":

    #MONGO_URI, DB_NAME 확인
    load_dotenv()  # .env 파일 로드

    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME") or "gemini_db"

    for var_name, var_value in [("MONGO_URI", MONGO_URI),
                                ("DB_NAME", DB_NAME)]:
        if not var_value:
            raise ValueError(f"{var_name}가 .env파일에 설정되어있지 않습니다.")
     # MongoDB 연결 생성
    db_connection = MongoDBConnection(MONGO_URI, DB_NAME)

    # .env에 JSON형태로 저장된 API KEY를 dict 형태로 불러오기
    AI_API_KEY = json.loads(os.getenv("AI_API_KEY"))
    ai_factory = AI_Factory(AI_API_KEY)

    # VectorStoreHandler 인스턴스 생성 (임베딩 모델 및 청크 설정은 필요에 따라 조정)
    vector_handler = VectorStoreHandler(chunk_size=500, chunk_overlap=50)
    
    #주제를 후에 입력받는다고 가정하고 작성.
    #토론 인스턴스 만들기
    participant_factory = ParticipantFactory(vector_handler,db_connection,ai_factory)
    debate = Debate(participant_factory=participant_factory)

    ###############################임시로 입력받는 테스트 코드

    ####임시 사용자
    user_name = "사용자"
    user_id = "temp_id_111111111"
    user = {"name"  : user_name,
            "_id"   : user_id,
            "ai"    : None
            }
    ####임시 사용자


    opponent_name = input("상대 이름 설정 : ")
    opponent_id = "temp_id_123456789"
    opponent_ai = input("ai 설정 - 현재 가능한 AI : GEMINI")
    opponent = {"name"  : opponent_name,
                "_id"   : opponent_id,
                "ai"    : opponent_ai
                }
    
    participants = {"pos" : user, "neg" : opponent}
    
    topic = input("주제 입력 : ")

    debate.create(topic, participants)
    ###############################임시로 입력받는 테스트 코드
    
    
    ###############################임시로 실행하는 테스트 코드
    while debate.debate["status"]["type"] != "end":
        print (debate.progress())
    ###############################임시로 실행하는 테스트 코드
