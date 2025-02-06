from datetime import datetime
import db_module
class Debate:
    def __init__(self, judge):
        self.judge = judge
        self.debate = {
            "_id" : None,
            "participants" : {
                "pro": None,
                "con": None
            },
            "topic" : None,
            "status" : {
                "type": None,
                "step": 0
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

    def __init__(self, judge, topic:str, participants:dict):
        __init__(judge)
        create(topic, participants)

    def __init__(self, judge, id:str):
        __init__(judge)
        self.debate["_id"] = id
        load()
        



    # 기존 진행중인 토론 load - 자신이 가진 키를 기준으로 load.
    def load(self, db_connection: MongoDBConnection):
        # db에서 기록된 토론 정보 불러와서 덮어쓰기.
        pass
        

    # 토론 생성
    #     토론 주제와 참여자를 받아와서 db에 등록
    def create(self, topic:str, participants:dict, db_connection: MongoDBConnection):
        if self.debate["_id"] == None:
            # 아직 생성되지 않은 id로 판단, 내부 정보 업데이트
            self.debate["topic"] = topic
            self.debate["participants"] = participants
            self.debate["status"] = {
                "type": "start",
                "step": 0
            }
            # db에 추가 이후 키를 받아와서 토론 키를 현재 debate에 등록
            self.debate["_id"] = "<여기에 insert해서 키 받아오는 코드 입력>"
            return True
        else : 
            #이미 생성된 토론이므로 return False
            return False

# 토론 진행
# 진행중일때:
#     발언 순서 관리
#     debate_turn_manager(debate_id)
#         현재 진행도? 확인(서론, 본론, 결론)
#         if 유저의 차례:
#             발언 입력 받기.
        
        
#         else if AI의 차례:
#             ai 발언 생성.
#             generate_ai_response(debate_id, object_id)

#         발언 기록
#         log_speech(debate_id, speeker, message)


    # 토론 종료
    def end(self):
        self.debate["status"] = {
            "type" : "end",
            "step" : 0
        }
        evaluate_debate()
        summarize()
        save()


    # 토론 판결
    def evaluate_debate(self):
        # self.judge 호출
        # 판결
        self.debate["result"] = None # 여기에 판결 코드 입력하기 True or False?
        pass



    # 진행된 토론 요약
    def summarize(summarize_model):
        # summarize_model 불러와서 요약하기
        summary = self.debate["summary"]
        summary["summarize_pro"] = "",
        summary["summarize_con"] = "",
        summary["summarize_argument"] = "",
        summary["summarize_verdict"] = ""

    #진행된 토론 db에 올리기
    def save(self, db_connection: MongoDBConnection):
        pass
