from .debate import ParticipantFactory, Debate
from db_module import MongoDBConnection
from vectorstore_module import VectorStoreHandler
class DebateManager:
    def __init__(self, participant_factory:ParticipantFactory, db_connection:MongoDBConnection, vector_handler:VectorStoreHandler):
        self.debatepool = {}
        self.participant_factory = participant_factory
        self.db_connection = db_connection,
        self.vector_handler = vector_handler

    def create_debate(self, pos_name:str, pos_ai:str, neg_name:str, neg_ai:str, topic:str):
        pos = {
            "name"  : pos_name,
            "_id"   : "temp_id_pospospos",
            "ai"    : pos_ai,
            "img"   : None
        }
        neg = {
            "name"  : neg_name,
            "_id"   : "temp_id_pospospos",
            "ai"    : neg_ai,
            "img"   : None
        }
        participants = {"pos":pos, "neg":neg}

        debate = Debate(participant_factory=self.participant_factory,
                        db_connection=self.db_connection,
                        vector_handler=self.vector_handler)
        debate.create(topic=topic, participants=participants)
        id = debate.debate["_id"]
        self.debatepool[id] = debate
        return id