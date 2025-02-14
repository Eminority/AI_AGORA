<<<<<<< HEAD
from call_gemini_module import GeminiAPI
import os
from dotenv import load_dotenv
import google.generativeai as genai
from db_module import MongoDBConnection
from vectorstore_module import VectorStoreHandler  # 벡터스토어 관련 모듈 임포트
=======
import sys
import os
from debate.ai_module.gemini import GeminiAPI
import json
from dotenv import load_dotenv
import google.generativeai as genai
from db_module import MongoDBConnection
from vectorstore_module import VectorStoreHandler  # 벡터스토어 관련 모듈
from debate.ai_module.ai_factory import AI_Factory
from debate.participants import ParticipantFactory 
from debate.debate import Debate
from debate.debate_manager import DebateManager
>>>>>>> 4e1d7eb89fae2b707d29402c21817c364bdfe930


if __name__ == "__main__":

<<<<<<< HEAD
    #GEMINI_API_KEY, MONGO_URI, DB_NAME 확인
    load_dotenv()  # .env 파일 로드
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME") or "gemini_db"

    for var_name, var_value in [("GEMINI_API_KEY", GEMINI_API_KEY),
                                ("MONGO_URI", MONGO_URI),
                                ("DB_NAME", DB_NAME)]:
        if not var_value:
            raise ValueError(f"{var_name}가 .env파일에 설정되어있지 않습니다.")

     # MongoDB 연결 생성
    db_connection = MongoDBConnection(MONGO_URI, DB_NAME)



    # VectorStoreHandler 인스턴스 생성 (임베딩 모델 및 청크 설정은 필요에 따라 조정)
    vector_handler = VectorStoreHandler(chunk_size=500, chunk_overlap=50)
    
    # AI 인스턴스 생성(하나의 AI가 다역을 진행하기 위해서는 여러개의 인스턴스가 필요함)
    judgeAI_1 = GeminiAPI(GEMINI_API_KEY, db_connection=db_connection)



    crawled_texts_for_topic = ["주제","크롤링","데이터","삽입"]
    crawled_texts_for_pleading_positiveside = ["찬성측의","변론을 위한","크롤링데이터 삽입"]
    crawled_texts_for_pleading_negativeside = ["반대측의","변론을 위한","크롤링데이터 삽입"]

    all_text_in_discussion = ["회의","모든","대화","내용"] #판사에게 집어넣기 위해.

    # 크롤링 자료를 벡터스토어에 저장 (FAISS 인스턴스 생성)
    judgeAI_1_vectorstore = vector_handler.vectorstoring_from_list(crawled_texts_for_topic)
    debatorAI_1_vectorstore = vector_handler.vectorstoring_from_list(crawled_texts_for_topic)



    # 1. 시스템 역할 설정 (예: 판사 역할)
    judgeAI_1.set_role("당신은 판사로 찬반 토론을 진행합니다.")
    

    #후에 입력 받는 것으로 정리
    user_prompt = "토론 주제에 대해서 간략하게 설명해줘."

    # 6. 벡터스토어 기반 컨텍스트를 포함한 Gemini API 응답 생성
    response_text_vs = judgeAI_1.generate_text_with_vectorstore(user_prompt, crawled_texts_for_topic, k=3, max_tokens=200)

    print("판사 (Gemini API with VectorStore):\n", response_text_vs)
    

    # 3. 사용자 프롬프트를 DB에 저장
    judgeAI_1.insert_prompt(user_prompt)

    
    # 4. Gemini API를 사용하여 기본 응답 생성
    response_text = judgeAI_1.generate_text(user_prompt)
    print("판사 (Gemini API):\n", response_text)
    
    # 5. 생성된 응답을 DB에 저장
    judgeAI_1.save_response_to_db("responses", user_prompt, response_text)


    

    # 7. Gemini API 및 MongoDB 연결 종료
    judgeAI_1.close_connection()
=======
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

    # VectorStoreHandler 인스턴스 생성 (임베딩 모델 및 청크 설정은 필요에 따라 조정)
    vector_handler = VectorStoreHandler(chunk_size=500, chunk_overlap=50)

    #주제를 후에 입력받는다고 가정하고 작성.
    #토론 인스턴스 만들기
    participant_factory = ParticipantFactory(vector_handler,ai_factory)
    debate = Debate(participant_factory=participant_factory, db_connection=db_connection)
    debate_manager = DebateManager(participant_factory=participant_factory, db_connection=db_connection)
    ###############################임시로 입력받는 테스트 코드

    ####임시 사용자
    # user_name = input("pos 이름 설정 : ")
    # user_id = "temp_id_111111111"
    # user_ai = input("ai 설정 - 현재 가능한 AI : GEMINI // 입력  :")
    user = {
        "_id": "67ac1d198f64bb663ade93b3",
        "name": "clock",
        "ai" : "GEMINI",
        "object_attribute": "Out of control, out of control, very angry speach tone",
        "create_time":  "2025-02-12T04:01:29.651Z",
        "img":None
        }
    ####임시 사용자


    opponent_name = input("상대 이름 설정 : ")
    opponent_id = "temp_id_123456789"
    opponent_ai = input("ai 설정 - 현재 가능한 AI : GEMINI // 입력  :")
    opponent = {"name"  : opponent_name,
                "_id"   : opponent_id,
                "ai"    : opponent_ai,
                "img" : None
                }
    
    participants = {"pos" : user, "neg" : opponent}
    
    topic = input("주제 입력 : ")


    debate_manager.create_debate(pos=user, neg=opponent, topic=topic)    
    debates = debate_manager.debatepool.values()
    ###############################임시로 입력받는 테스트 코드
    
    
    ###############################임시로 실행하는 테스트 코드
    for debate in debates:
        while debate.debate["status"]["type"] != "end":
            print (debate.progress())
    ###############################임시로 실행하는 테스트 코드
>>>>>>> 4e1d7eb89fae2b707d29402c21817c364bdfe930
