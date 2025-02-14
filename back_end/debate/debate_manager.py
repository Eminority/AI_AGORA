from .debate import ParticipantFactory, Debate
from db_module import MongoDBConnection
from vectorstore_module import VectorStoreHandler

class DebateManager:
    def __init__(self, participant_factory:ParticipantFactory, db_connection:MongoDBConnection):
        self.debatepool = {}
        self.participant_factory = participant_factory
        self.db_connection = db_connection

    def create_debate(self, pos:dict, neg:dict, topic:str):
        if pos.get("_id"):
            pos["_id"] = str(pos["_id"])
        if neg.get("_id"):
            neg["_id"] = str(neg["_id"])
        participants = {"pos":pos, "neg":neg}

        debate = Debate(participant_factory=self.participant_factory,
                        db_connection=self.db_connection)
        
        debate.create(topic=topic, participants=participants)
        id = str(debate.debate["_id"])
        self.debatepool[id] = debate
        return id