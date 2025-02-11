from fastapi import FastAPI, HTTPException
import os
import json
from dotenv import load_dotenv
from debate.ai_module.ai_factory import AI_Factory
from debate.debate_manager import DebateManager
from debate.participants import ParticipantFactory
from db_module import MongoDBConnection
from vectorstore_module import VectorStoreHandler

# 환경 변수 로드
load_dotenv()

# MongoDB 연결
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URI or not DB_NAME:
    raise ValueError("MONGO_URI 또는 DB_NAME이 .env 파일에서 설정되지 않았습니다.")

db_connection = MongoDBConnection(MONGO_URI, DB_NAME)

# AI API 키 불러오기
AI_API_KEY = json.loads(os.getenv("AI_API_KEY"))
ai_factory = AI_Factory(AI_API_KEY)

# 벡터스토어 핸들러 생성
vector_handler = VectorStoreHandler(chunk_size=500, chunk_overlap=50)


# Debate 인스턴스 초기화
participant_factory = ParticipantFactory(vector_handler, ai_factory)

# FastAPI 앱 생성
app = FastAPI()

#토론 관리 인스턴스 생성
debateManager = DebateManager(participant_factory=participant_factory, db_connection=db_connection)

# 토론 생성 API
@app.post("/debate")
def create_debate(pos_name: str, pos_ai: str, neg_name: str, neg_ai: str, topic: str):
    debate_id = debateManager.create_debate(pos_name, pos_ai, neg_name, neg_ai, topic)
    return {"message": "토론이 생성되었습니다.", "topic": topic, "id":debate_id}

# 토론 상태 확인 API
@app.get("/debate/status")
def get_debate_status(id:str):
    return debateManager.debatepool[id].debate["status"]

# 토론 진행 API
@app.post("/debate/progress")
def progress_debate(id:str):
    if debateManager.debatepool[id].debate["status"]["type"] == "end":
        return {"message": "토론이 이미 종료되었습니다."}
    
    return {"progress": debateManager.debatepool[id].progress()}

@app.get("debate/list")
def get_debate_list():
    debatelist = {}
    for id in debateManager.debatepool.keys():
        debatelist[id] = debateManager.debatepool[id]["debate"]["topic"]
    return debatelist

##실행코드
# uvicorn backserver:app --host 0.0.0.0 --port 8000 --reload