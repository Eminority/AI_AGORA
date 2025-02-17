## ai 프로필을 만들어서 저장하고 불러올 수 있게끔 하는 모듈
from db_module import MongoDBConnection
from datetime import datetime
from detect_persona import DetectPersona
class ProfileManager:
    def __init__(self, db: MongoDBConnection, persona_module:DetectPersona):
        data = db.select_data_from_query(collection_name="object", query={})
<<<<<<< HEAD
=======
        self.db = db
>>>>>>> dev0
        self.objectlist = {}
        self.persona_module = persona_module
        for raw_object in data:
            profile = Profile(_id           = str(raw_object.get("_id")),
                          name              = raw_object.get("name"),
                          img               = raw_object.get("img"),
                          ai                = raw_object.get("ai"),
                          create_time       = raw_object.get("create_time"),
                          object_attribute  = raw_object.get("object_attribute"),
                          debate_history    = raw_object.get("debate_history", [])
                          )
            if str(raw_object.get("_id")):
                self.objectlist[profile.data["_id"]] = profile

    def create_profile(self,
                        name:str=None,
                        img:str=None,
                        ai:str=None):
        if not self.duplicate_object_check(name):
            return {"result":False}
        object_attribute = self.persona_module.get_traits(name)
        new_obj = Profile(name=name,
                            img=img,
                            ai=ai,
                            object_attribute=object_attribute,
                            create_time=datetime.now()
                            )
        new_obj.save(self.db)
        print(new_obj.data)
        self.objectlist[new_obj.data["_id"]] = new_obj
        return {"result":True, "id":new_obj.data["_id"]}
    
    def duplicate_object_check(self, name:str):
        """
        참이면 중복없음
        거짓이면 중복있음
        """
        search_result = self.db.select_data_from_query("object",{"name":name})
        print(search_result)
        if not search_result:
            return True
        else:
            return False

    
class Profile:
    def __init__(self, _id:str=None,
                        name:str=None,
                        img:str=None,
                        ai:str=None,
                        create_time:str=None,
                        object_attribute:str=None,
                        debate_history:list=[]):
        self.data = {}
        self.data["name"]           = name
        self.data["img"]            = img
        self.data["ai"]             = ai
        self.data["create_time"]    = create_time
        self.data["object_attribute"] = object_attribute
        self.data["debate_history"] = debate_history
        if _id: # id가 None으로라도 들어가있으면 에러 내니까 None이면 아예 안만들기
            self.data["_id"]        = _id

    def save(self, db:MongoDBConnection):
        if self.data.get("_id"): #_id가 이미 있는 경우 update
            db.update_data("object", self.data)
        else : #_id가 없는 경우 insert하고 self id저장
            self.data["_id"] = db.insert_data("object", self.data)