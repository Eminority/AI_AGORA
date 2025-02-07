from db_module import MongoDBConnection
from agora_ai import Agora_AI

class ParticipantFactory:
    def __init__(self, vector_handler: VectorStoreHandler, db_connection: MongoDBConnection, ai_api:dict):
        self.vector_handler = vector_handler,
        self.db_connection = db_connection
        self.ai_api = ai_api # "GEMINI" : "GEMINI_API" 같은 형식의 dict

    def make_participant(self, data:dict=None):
        ai_type = data["ai"]
        agora_ai = None
        if ai_type in self.ai_api:
            agora_ai = Agora_AI(ai_type, self.ai_api[ai_type], self.vector_handler)
        return Participant(id = data["_id"], name = data["name"], ai = agora_ai, img = data["img"])

class Participant:
    #db에서의 _id, name, 사용할 ai, 프로필 사진을 받아오기.
    def __init__(self, id:str, name:str = None, ai:Agora_AI=None, img = None):
        self.id = id
        self.name = name
        self.ai = ai
        self.img = img

    def answer(self, prompt:str = None):
        # ai가 아닌 경우 = 사람인 경우
        if not self.ai:
            #외부에서 답변 받아와서 리턴
            pass
        else:
            #ai인 경우
            return ai.generate_text(prompt, [])

    

