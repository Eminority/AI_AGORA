import os
from dotenv import load_dotenv
from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, uri: str, db_name: str):
        """
        MongoDB 연결을 위한 초기화.
        :param uri: MongoDB 연결 URI
        :param db_name: 사용할 데이터베이스 이름
        """
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]

            self.client.admin.command('ping')
            print("DB Connection Successed")
        except Exception as e:
            print("Connection failed: ", e)

    def insert_conversation(self, collection_name: str, data: dict) -> str:
        """
        대화 내용을 MongoDB에 저장.
        :param collection_name: 컬렉션 이름
        :param data: 저장할 데이터(dict)
        :return: 생성된 문서의 ObjectID를 문자열로 반환
        """
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def close_connection(self):
        """
        MongoDB 연결 종료
        """
        self.client.close()

if __name__ == "__main__":
    load_dotenv()  # .env 파일 로드
    # 예시로 .env에서 URI와 DB_NAME을 불러온다고 가정
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")

    if not MONGO_URI or not DB_NAME:
        raise ValueError("MONGO_URI or DB_NAME is not set in the .env file")

    db_connection = MongoDBConnection(MONGO_URI, DB_NAME)

    # 예시 데이터 삽입
    """
    example_data = {"message": "Hello, MongoDB!"}
    inserted_id = db_connection.insert_conversation("test_collection", example_data)
    print("Inserted document ID:", inserted_id)

    """
    db_connection.close_connection()