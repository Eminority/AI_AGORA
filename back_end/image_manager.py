import base64
from fastapi import UploadFile, File
from db_module import MongoDBConnection
from datetime import datetime
import shutil
class ImageManager:
    def __init__(self, db:MongoDBConnection, img_path:str):
        self.db = db
        self.img_path = img_path

    def save_image_in_mongoDB(self, file: UploadFile=File(...)) -> dict:
        image_data = file.file.read()
        encoded_string = base64.b64encode(image_data).decode('utf-8')

        image_data = {"filename" : f"{datetime.now()}_{file.filename}", "data": encoded_string}
        result = self.db.insert_data('image', image_data)
        return {"file_id": str(result), "filename": image_data['filename']}

    def save_image_in_local_from_mongoDB(self, file_id:str) -> dict:
        try:
            image_data = self.db.select_data_from_id('image', file_id)

            if not image_data:
                return {"error": "File not found"}
            
            image = base64.b64decode(image_data["data"])
            with open(f"{self.img_path}/{image_data['filename']}", "wb") as file:
                file.write(image)
            return {"result":True, "data": f"{self.img_path}/{image_data['filename']}"}
        
        except Exception as e:
            return {"result":False, "data":e}
        
    def save_image_in_local_from_form(self, file:UploadFile=File(...)) -> dict:
        save_path = f"{self.img_path}/{datetime.now()}_{file.filename}.png"
        try:
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return {"result":True, "data":save_path}
        except Exception as e:
            return {"result":False, "data":e}