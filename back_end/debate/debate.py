import uuid
import time
from datetime import datetime
from db_module import MongoDBConnection
from .participants import ParticipantFactory
from .agora_ai import Agora_AI

class Debate:
    def __init__(self, participant_factory: ParticipantFactory = None, db_connection: MongoDBConnection = None, vector_handler=None):
        self.judge = None
        self.pos = None
        self.neg = None
        self.db_connection = db_connection
        self.participant_factory = participant_factory
        self.vector_handler = vector_handler

        # debate 필드 초기화
        self.debate = {
            "_id": None,
            "participants": None,
            "topic": None,
            "status": {
                "type": None,  # "in_progress" 또는 "end" 등
                "step": 0,     # 1부터 11까지 단계
                "turn": None
            },
            "debate_log": [],
            "start_time": None,
            "end_time": None,
            "summary": {
                "summary_pos": None,
                "summary_neg": None,
                "summary_arguments": None,
                "summary_verdict": None
            },
            "result": None
        }

        # 총 11단계 진행
        self.max_step = 11

    def set_judge(self):
        """판사 역할의 AI 인스턴스 생성 및 역할 설정"""
        gemini_instance = self.participant_factory.ai_factory.create_ai_instance("GEMINI")
        self.judge = Agora_AI(ai_type="GEMINI", ai_instance=gemini_instance, vector_handler=self.vector_handler)
        self.judge.set_role("judge")

    def create(self, topic: str, participants: dict):
        """
        토론 생성: 새로운 토론(_id, topic, participants 등) 정보를 세팅하고
        DB에 저장한 뒤, 판사와 참가자들을 준비합니다.
        """
        if self.debate["_id"] is not None or not participants:
            return False

        self.debate["topic"] = topic
        self.debate["participants"] = participants
        self.debate["status"] = {
            "type": "in_progress",  # 토론을 시작할 때 바로 in_progress로 설정
            "step": 1,              # 1단계부터 진행
            "turn": None
        }

        # _id 필드를 UUID로 생성하여 할당
        self.debate["_id"] = str(uuid.uuid4())

        # DB에 삽입 후 실제 _id(또는 ObjectId) 값을 debate dict에 반영
        debate_id = self.db_connection.insert_data("debate", self.debate)
        self.debate["_id"] = debate_id

        # 참가자 생성 (pos, neg)
        self.pos = self.participant_factory.make_participant(participants["pos"])
        self.neg = self.participant_factory.make_participant(participants["neg"])

        # 판사 생성 및 등록
        self.set_judge()

        return True

    def progress(self):
        """
        11단계 순서:
          1) 판사가 주제 설명
          2) 찬성측 주장
          3) 반대측 주장
          4) 판사가 변론 준비시간(1초) 부여
          5) 반대측 변론
          6) 찬성측 변론
          7) 판사가 최종 주장 시간(1초) 부여
          8) 찬성측 최종 결론
          9) 반대측 최종 결론
          10) 판사가 판결 준비시간(1초) 부여
          11) 판사 최종 결론 (evaluate)
        """
        debate = self.debate
        result = {"timestamp": None, "speaker": "", "message": ""}

        # 유효하지 않은 토론이면 메시지 반환
        if debate["_id"] is None:
            result["speaker"] = "SYSTEM"
            result["message"] = "유효하지 않은 토론입니다."
            result["timestamp"] = datetime.now()
            return result

        # 단계(step)가 설정되어 있지 않다면 1로 초기화
        if "step" not in debate["status"]:
            debate["status"]["step"] = 1
        step = debate["status"]["step"]

        # 단계별 로직
        if step == 1:
            # 1. 판사가 주제 설명
            # (필요시 토론 준비 작업)
            self.ready_to_debate()
            result["speaker"] = "judge"
            result["message"] = self.judge.generate_text("System:judge\nContext:topic\nUser:Tell me about the gist of the argument")

        elif step == 2:
            # 2. 찬성측 주장
            result["speaker"] = "pos"
            result["message"] = self.pos.answer("System:positive\nContext:Comments in favor of the topic\nUser:tell me your opinion on the topic, including supporting evidence.")

        elif step == 3:
            # 3. 반대측 주장
            result["speaker"] = "neg"
            result["message"] = self.neg.answer("반대측 주장 발언 프롬프트")

        elif step == 4:
            # 4. 판사가 변론 준비시간 1초 제공
            result["speaker"] = "judge"
            result["message"] = "변론 준비 시간 1초를 갖겠습니다."
            time.sleep(1)

        elif step == 5:
            # 5. 반대측 변론
            result["speaker"] = "neg"
            result["message"] = self.neg.answer("반대측 변론 프롬프트")

        elif step == 6:
            # 6. 찬성측 변론
            result["speaker"] = "pos"
            result["message"] = self.pos.answer("찬성측 변론 프롬프트")

        elif step == 7:
            # 7. 판사가 최종 주장 시간(1초) 부여
            result["speaker"] = "judge"
            result["message"] = "최종 주장 준비 시간 1초를 갖겠습니다."
            time.sleep(1)

        elif step == 8:
            # 8. 찬성측 최종 결론
            result["speaker"] = "pos"
            result["message"] = self.pos.answer("찬성측 최종 결론 프롬프트")

        elif step == 9:
            # 9. 반대측 최종 결론
            result["speaker"] = "neg"
            result["message"] = self.neg.answer("반대측 최종 결론 프롬프트")

        elif step == 10:
            # 10. 판사가 판결 준비시간(1초) 부여
            result["speaker"] = "judge"
            result["message"] = "판결 준비 시간 1초를 갖겠습니다."
            time.sleep(1)

        elif step == 11:
            # 11. 판사가 최종 결론
            result["speaker"] = "judge"
            result["message"] = self.evaluate()  # evaluate() 내부에서 self.summarize() 등 수행
            # 모든 단계가 끝났으므로 토론 종료
            debate["status"]["type"] = "end"

        else:
            # 1~11 범위를 벗어난 경우
            result["speaker"] = "SYSTEM"
            result["message"] = "이미 모든 토론 단계가 종료되었습니다."

        # 로그에 기록
        debate["debate_log"].append(result)
        result["timestamp"] = datetime.now()
        # self.save()

        # 아직 11단계가 아니면 다음 단계로 증가
        if step < self.max_step:
            debate["status"]["step"] += 1

        return result

    def ready_to_debate(self):
        """참가자와 판사가 토론 주제에 대해 미리 자료 수집/준비를 수행"""
        topic = self.debate["topic"]
        if self.pos and hasattr(self.pos, 'agora_ai'):
            self.pos.agora_ai.crawling(topic)
        if self.neg and hasattr(self.neg, 'agora_ai'):
            self.neg.agora_ai.crawling(topic)
        if self.judge:
            self.judge.crawling(topic)

    def evaluate(self):
        """판사가 최종 판결문(결론)을 생성하고, 토론 내용을 요약"""
        self.debate["result"] = self.judge.generate_text("판사의 최종 판결문 요청 프롬프트")
        self.summarize()
        return self.debate["result"]

    def summarize(self):
        """토론 내용을 요약(필요 시 요약 로직 적용 가능)"""
        summary = self.debate["summary"]
        summary["summary_pos"] = ""
        summary["summary_neg"] = ""
        summary["summary_arguments"] = ""
        summary["summary_verdict"] = ""

    def load(self):
        """데이터베이스에서 저장된 토론 정보를 불러와 현재 객체에 저장"""
        try:
            self.debate = self.db_connection.select_data_from_id("debate", self.debate["_id"])
        except Exception as e:
            print("load failed:", e)
            return False
        return True

    def save(self):
        """현재 토론 상태를 데이터베이스에 업데이트하여 저장"""
        self.db_connection.update_data("debate", self.debate)
