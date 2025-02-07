import db_module

class Participant:
    #db에서의 _id, name, 사용할 ai, 프로필 사진을 받아오기.
    def __init__(self, id:str, name:str = None, ai = None, img = None, db_connection :MongoDBConnection = None):
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
            #해당 ai에서 답변 받아와 리턴
            pass

        

    

