from db_module import MongoDBConnection
from agora_ai import Agora_AI
from ai_module.ai_factory import AI_Factory
class ParticipantFactory:
    def __init__(self, vector_handler: VectorStoreHandler, db_connection: MongoDBConnection, ai_factory:AI_Factory):
        self.vector_handler = vector_handler,
        self.db_connection = db_connection
        self.ai_factory = ai_factory

    def make_participant(self, data:dict=None):
        ai_type = data["ai"]
        # ai type을 기반으로 instance 만들어주기
        ai_instance = self.ai_factory.create_ai_instance(ai_type)
        #만들어진 ai instance를 참가자 형태로 만들기
        agora_ai = Agora_AI(ai_type, ai_instance, self.vector_handler)
        return Participant(id = data["_id"], name = data["name"], ai = agora_ai, img = data["img"])

class Participant:
    #db에서의 _id, name, 사용할 ai, 프로필 사진을 받아오기.
    def __init__(self, id:str, name:str = None, agora_ai:Agora_AI = None, img = None):
        self.id = id
        self.name = name
        self.agora_ai = agora_ai
        self.img = img

    def answer(self, prompt:str = None):
        # ai가 아닌 경우 = 사람인 경우
        if not self.agora_ai:
            #외부에서 답변 받아와서 리턴
            pass
        else:
            #ai인 경우
            return agora_ai.generate_text(prompt, [])

    

