from datetime import datetime
from db_module import MongoDBConnection
from .participants import ParticipantFactory
from .agora_ai import Agora_AI
import uuid
class Debate:
    def __init__(self, participant_factory: ParticipantFactory = None, db_connection: MongoDBConnection = None, vector_handler=None):
        # [리팩토링] 중복된 import 제거 및 debate 필드 초기화
        # _id와 participants를 None으로 초기화하여 유효성 검증 시 활용합니다.
        self.judge = None
        self.pos = None
        self.neg = None
        self.db_connection = db_connection
        self.participant_factory = participant_factory
        self.vector_handler = vector_handler
        self.debate = {
            "_id": None,  # 기존의 built-in id 사용 오류 수정
            "participants": None,  # 참가자 정보를 명시적으로 초기화
            "topic": None,
            "status": {"type": None, "step": 0, "turn": None},
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
        # 오고 가는 최대 대화 수 (서론, 본론, 결론 3단계)
        self.max_step = 3

    def set_judge(self):
        # [리팩토링] 판사 역할의 AI 인스턴스 생성 및 역할 설정
        gemini_instance = self.participant_factory.ai_factory.create_ai_instance("GEMINI")
        self.judge = Agora_AI(ai_type="GEMINI", ai_instance=gemini_instance, vector_handler=self.vector_handler)
        self.judge.set_role("judge")

    def progress(self):
        # [리팩토링] 현재 토론 진행 상황에 따라 적절한 발언을 생성
        debate = self.debate
        result = {"timestamp": None, "speaker": "", "message": ""}
        
        # _id가 없으면 유효하지 않은 토론으로 판단
        if debate["_id"] is None:
            result["speaker"] = "SYSTEM"
            result["message"] = "유효하지 않은 토론"
            result["timestamp"] = datetime.now()
            return result

        status = debate["status"]
        if status["type"] == "start":
            # 토론 시작 단계: 참가자와 판사 준비 후 판사가 주제를 소개
            self.ready_to_debate()  # 참가자와 판사의 준비 작업 수행
            result["speaker"] = "judge"
            result["message"] = self.judge.generate_text("주제에 대해 말해달라는 프롬프트")
            self.next_turn()  # 다음 발언 순서로 전환
        elif status["type"] == "in_progress":
            # 토론 진행 중: 현재 발언 차례인 참가자가 발언
            if status["turn"] == "pos":
                result["speaker"] = "pos"
                result["message"] = self.pos.answer("찬성측 발언 요청 프롬프트")
            elif status["turn"] == "neg":
                result["speaker"] = "neg"
                result["message"] = self.neg.answer("반대측 발언 요청 프롬프트")
                
            elif status["turn"] == "judge":
                result["speaker"] = "judge"
                result["message"] = self.judge.generate_text("판사측 발언 요청 프롬프트")
            self.next_turn()  # 발언 후 다음 순서로 전환
        elif status["type"] == "end":
            # 토론 종료 단계: 판사가 최종 판결문 생성
            result["speaker"] = "judge"
            result["message"] = self.evaluate()
        
        # 발언 내역을 토론 로그에 추가
        debate["debate_log"].append(result)
        result["timestamp"] = datetime.now()
        return result

    def ready_to_debate(self):
        # [리팩토링] 참가자 및 판사가 토론 주제에 맞게 준비 작업 수행
        if self.pos and hasattr(self.pos, 'agora_ai'):
            self.pos.agora_ai.crawling(self.debate["topic"])
        if self.neg and hasattr(self.neg, 'agora_ai'):
            self.neg.agora_ai.crawling(self.debate["topic"])
        if self.judge:
            self.judge.crawling(self.debate["topic"])

    def next_turn(self):
        # [리팩토링] 발언 순서를 명확하게 정의 및 진행 단계 관리
        status = self.debate["status"]
        if status["type"] == "start":
            # 시작 단계에서 in_progress 상태로 전환하며 찬성측부터 발언 시작
            status["type"] = "in_progress"
            status["turn"] = "pos"
            status["step"] += 1
        elif status["type"] == "in_progress":
            # 현재 발언 차례에 따라 다음 발언자로 순환
            if status["turn"] == "pos":
                status["turn"] = "neg"
            elif status["turn"] == "neg":
                status["turn"] = "judge"
            elif status["turn"] == "judge":
                status["turn"] = "pos"
                status["step"] += 1  # 한 사이클(찬성, 반대, 판사) 완료 후 진행 단계 증가
            # 진행 단계가 최대 단계에 도달하면 토론을 종료
            if status["step"] >= self.max_step:
                status["type"] = "end"

    def load(self):
        # [리팩토링] 데이터베이스에서 저장된 토론 정보를 불러와 현재 객체에 덮어씌움
        try:
            self.debate = self.db_connection.select_data_from_id("debate", self.debate["_id"])
        except Exception as e:
            print("load failed:", e)
            return False
        return True

    def create(self, topic: str, participants: dict):
        # [리팩토링] 토론 생성 시 기존에 생성된 토론이 없는지 및 참가자 정보 유효성을 확인
        if self.debate["_id"] is not None or not participants:
            return False
        self.debate["topic"] = topic
        self.debate["participants"] = participants
        self.debate["status"] = {"type": "start", "step": 0, "turn": None}
        
        # _id 필드를 UUID로 생성하여 할당
        self.debate["_id"] = str(uuid.uuid4())
        # 데이터베이스에 토론 정보를 삽입 후 생성된 토론 ID를 저장
        debate_id = self.db_connection.insert_data("debate", self.debate)
        
        # 참가자 생성 (예: "pos"와 "neg"로 구분) 후 각각 할당
        self.pos = self.participant_factory.make_participant(participants["pos"])
        self.neg = self.participant_factory.make_participant(participants["neg"])
        self.debate["_id"] = debate_id
        
        # 판사 생성 및 등록
        self.set_judge()
        return True

    def evaluate(self):
        # [리팩토링] 판사가 최종 판결문(토론 결과)을 생성하고, 토론 내용을 요약
        self.debate["result"] = self.judge.generate_text("판결문을 달라는 프롬프트 입력")
        self.summarize()
        return self.debate["result"]

    def summarize(self):
        # [리팩토링] 토론 요약 정보를 초기화(필요 시 요약 모델을 적용할 수 있음)
        summary = self.debate["summary"]
        summary["summary_pos"] = ""
        summary["summary_neg"] = ""
        summary["summary_arguments"] = ""
        summary["summary_verdict"] = ""

    def save(self):
        # [리팩토링] 현재 토론 상태를 데이터베이스에 업데이트하여 저장
        self.db_connection.update_data("debate", self.debate)
