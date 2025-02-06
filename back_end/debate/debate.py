from datetime import datetime
import db_module
class Debate:
    def __init__(self, judge, topic:str = None, participants: dict = None, id: str = None):
        self.judge = judge
        self.debate = {
            "_id" : id,
            "participants" : participants,
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
        if id:
            self.load()
        elif topic and participants:
            self.create(topic, participants)
        
        if not participants:
            self.debate["participants"] = {"pro":None, "con":None}
        



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
            debate_id = db_connection.insert_conversation("debate", self.debate)
            self.debate["_id"] = debate_id
            return True
        else : 
            #이미 생성된 토론이므로 return False
            return False

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

    #토론이 종료되면
    #   end()
    #   save(db_connect)


    # 토론 종료
    def end(self):
        self.debate["status"] = {
            "type" : "end",
            "step" : 0
        }
        evaluate()
        summarize()


    # 토론 판결
    def evaluate(self):
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
        db_connection.update_data("debate", self.debate)
