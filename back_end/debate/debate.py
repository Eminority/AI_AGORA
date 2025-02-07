from datetime import datetime
from db_module import MongoDBConnection
from participants import Participant, ParticipantFactory
from agora_ai import Agora_AI
from datetime import datetime
class Debate:
    def __init__(self, topic:str = None, participants: dict = None, id: str = None, participant_factory:ParticipantFactory = None, db_connection:MongoDBConnection = None):
        self.pos = None
        self.neg = None
        self.db_connection = db_connection
        self.debate = {
            "_id" : id,
            "participants" : participants,
            "topic" : None,
            "status" : {
                "type": None, 
                "step": 0,
                "turn": None
            },
            "debate_log": [],
            "start_time": None,
            "end_time": None,
            "summary": {
                "summary_pro":None,
                "summary_con":None,
                "summary_arguments": None,
                "summary_verdict": None
            },
            "result": None
        }
        # 아이디가 있으면 - 아이디 기반으로 토론 정보 로드
        if id:
            self.load()
        elif topic and participants: #주제, 참가자만 있으면 그걸로 생성
            self.create(topic, participants)

        #참가자가 존재하는 경우 참가자를 객체화해서 가지고 있기
        if participants:
            self.pos = participant_factory.make_participant(participants["pos"])
            self.neg = participant_factory.make_participant(participants["neg"])
        else :
            self.debate["participants"] = {"pos":None, "neg":None}

        #판사 정의
        gemini_instance = participant_factory.ai_factory.create_ai_instance("GEMINI")
        self.judge = Agora_AI(gemini_instance, vectorhandler=self.vector_handler)
        self.judge.set_role("judge")
        
        #오고 갈 최대 대화 수 정하기
        #서론 본론 결론으로 생각해서 일단은 3으로
        self.max_step = 3


    #id 받아와서 객체로 만들기
    def make_participant(data):
        return Participant(data["_id"], data["name"], data["ai"], data["img"])
    
# 토론 진행
# 진행중일때:
#   발언 순서 관리
#   debate_turn_manager()
#       현재 진행도? 확인(서론, 본론, 결론)
#       if 유저의 차례:
#           발언 입력 받기.      
#           else if AI의 차례:
#               ai 발언 생성.
#               prompt = "<입력할 프롬프트>"
#               ai.generete_text(prompt)

#         발언 기록
#         log_speech(debate_id, speeker, message)

    def progress(self, db_connection: MongoDBConnection):
        # self.debate를 절차에 맞게 수정
        # 이후 return self.debate
        debate = self.debate
        # 반환할 내용에는 발언자와 내용, 시간이 있어야함.
        result = {"timestamp":"","speaker": "", "message":""}
        if not debate["_id"]:
            # 등록된 아이디가 없으면
            # 주제를 입력받기
            # 토론 참여자 선택하기
            # 입력받은 주제를 가지고 토론 생성하기
            self.create(topic="입력받은 주제", participants={"여기에 찬성 측, 반대 측 입력"}, db_connection=db_connection)
        else:
            # 등록된 아이디가 있는 경우
            # 현재 상태 확인
            status = debate["status"]
            if status["type"] == "start":
                # 토론이 주제와 참가자를 받아 생성된 상태일 때
                # 토론 준비 시키기
                self.ready_to_debate()
                #준비가 끝났다면 판사가 주제를 간단하게 말하게 하기
                result["speaker"] = "judge"
                result["message"] = self.judge.generate_text("주제에 대해 말해달라는 프롬프트")
                #토론을 시작으로 상태 변경
                self.next_turn()
            elif status["type"] == "in_progress":
                # 토론이 진행중인 경우
                # status["step"]:int 에 따라서 진행도 생각하기

                # 현재 차례인 쪽에게서 답변 받기
                # AI 차례라면 적절한 AI에게서 답변 생성
                if status["turn"] == "pos":
                    result["speaker"] = "pos"
                    result["message"] = self.pos.answer("찬성측 발언 요청 프롬프트")
                elif status["turn"] == "neg":
                    result["speaker"] = "neg"
                    result["message"] = self.neg.answer("반대측 발언 요청 프롬프트")
                    pass
                elif status["turn"] == "judge":
                    result["speaker"] = "judge"
                    result["message"] = self.judge.generate_text("판사측 발언 요청 프롬프트")
                #차례 넘기기
                self.next_turn()
            elif status["type"] == "end":
                #토론이 끝난 경우
                #토론 판결
                self.end()
                self.evaluate()
            result["timestamp"] = datetime.now()
            self.debate["debate_log"].append(result)
        return result

    # 참가자들 준비시키기
    def ready_to_debate():
        #참가자가 AI라면 준비(크롤링)시키기
        if self.pos.agora_ai:
            self.pos.agora_ai.crawling(self.debate["topic"])
        if self.neg.agora_ai:
            self.neg.agora_ai.crawling(self.debate["topic"])
        #판사도 크롤링시키기
        self.judge.crawling(self.debate["topic"])
        

    #토론 다음 순서로 넘기기
    def next_turn():
        status = self.debate["status"]
        if status["type"] == "start":
            status["type"] = "in_progress"
        elif status["type"] == "in_progress" and status["turn"] >= self.max_step:
            status["type"] = "end"
        #대화 순서 정하기
        if status["turn"] == None or "judge":
            status["turn"] = "pos" #판사 또는 발언 전이라면 찬성측
            #진행도 +1
            status["step"] += 1
        elif status["turn"] == "pos":
            status["turn"] = "neg" #찬성측 발언 후에는 반대측
        elif status["turn"] == "neg":
            status["turn"] = "judge" #반대측 발언 후에는 판사 정리발언?

        

    # 기존 진행중인 토론 load - 자신이 가진 키를 기준으로 load.
    def load(self, db_connection: MongoDBConnection):
        # db에서 기록된 토론 정보 불러와서 덮어쓰기.
        try:
            self.debate = db_connection.select_data_from_id("debate", self.debate["_id"])
        except Exception as e :
            print("load failed : ", e)
            return False
        
        return True

    # 토론 생성
    #     토론 주제와 참여자를 받아와서 db에 등록
    def create(self, topic:str, participants:dict):
        if self.debate["_id"] == None:
            # 아직 생성되지 않은 id로 판단, 내부 정보 업데이트
            self.debate["topic"] = topic
            self.debate["participants"] = participants
            self.debate["status"] = {
                "type": "start",
                "step": 0
            }
            # db에 추가 이후 키를 받아와서 토론 키를 현재 debate에 등록
            debate_id = self.db_connection.insert_data("debate", self.debate)
            self.make_participant(participants)
            self.debate["_id"] = debate_id
            return True
        else : 
            #이미 생성된 토론이므로 return False
            return False

    # 토론 종료
    def end(self):
        self.debate["status"] = {
            "type" : "end",
            "step" : 0
        }

    # 토론 판결
    def evaluate(self):
        self.debate["result"] = self.judge.generate_text("판결문을 달라는 프롬프트 입력")
        self.summarize()



    # 진행된 토론 요약
    def summarize(summarize_model):
        # summarize_model 불러와서 요약하기
        summary = self.debate["summary"]
        summary["summarize_pos"] = "",
        summary["summarize_neg"] = "",
        summary["summarize_argument"] = "",
        summary["summarize_verdict"] = ""

    #진행된 토론 db에 올리기
    def save(self, db_connection: MongoDBConnection):
        db_connection.update_data("debate", self.debate)
