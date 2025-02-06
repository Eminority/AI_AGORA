import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from db_module import MongoDBConnection
from vectorstore_module import VectorStoreHandler  # 벡터스토어 관련 모듈 임포트

# GeminiAPI: 기존 Gemini API를 사용하며, 벡터스토어 기반 컨텍스트 활용 기능을 추가합니다.


class GeminiAPI:
    def __init__(self, api_key: str, db_connection: MongoDBConnection = None):
        """
        Gemini API 클라이언트를 초기화하고 선택적으로 MongoDB에 연결합니다.
        
        :param api_key: Google Gemini API 키
        :param db_connection: MongoDBConnection 인스턴스 (선택 사항)
        """
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.role = ""  # 기본 시스템 역할 (없으면 빈 문자열)
        
        self.db_connection = db_connection
        self.db = self.db_connection.db if self.db_connection else None

    def set_role(self, role_text: str):
        """
        시스템 역할을 설정하여 모든 프롬프트에 선행하는 지침으로 사용합니다.
        
        :param role_text: 시스템 역할 또는 지침 텍스트
        """
        self.role = role_text
        print("시스템 역할이 설정되었습니다.")

    def generate_text(self, user_prompt: str, max_tokens: int = 200) -> str:
        """
        Gemini 모델을 사용하여 기본 텍스트를 생성합니다.
        
        :param user_prompt: 사용자 입력 프롬프트
        :param max_tokens: 생성할 최대 토큰 수
        :return: 생성된 텍스트
        """
        full_prompt = user_prompt
        if self.role:
            full_prompt = f"System: {self.role}\nUser: {user_prompt}"
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={"max_output_tokens": max_tokens}
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_text_with_vectorstore(self, user_prompt: str, vectorstore, k: int = 3, max_tokens: int = 200) -> str:
        """
        벡터스토어에서 관련 컨텍스트를 검색한 후, 이를 포함하여 Gemini API로 답변을 생성합니다.
        
        :param user_prompt: 사용자 입력 프롬프트
        :param vectorstore: FAISS 벡터스토어 인스턴스 (예: 주제 자료가 저장된 벡터스토어)
        :param k: 유사도 검색 시 반환할 문서 수 (기본값: 3)
        :param max_tokens: 생성할 최대 토큰 수
        :return: 생성된 텍스트
        """
        try:
            # 벡터스토어에서 유사 문서 검색 (각 문서는 page_content 속성을 가짐)
            search_results = vectorstore.similarity_search(user_prompt, k=k)
            context = "\n".join([doc.page_content for doc in search_results])
        except Exception as e:
            context = ""
            print(f"벡터스토어 검색 실패: {e}")

        if self.role:
            full_prompt = f"System: {self.role}\nContext: {context}\nUser: {user_prompt}"
        else:
            full_prompt = f"Context: {context}\nUser: {user_prompt}"
            
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={"max_output_tokens": max_tokens}
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    def insert_prompt(self, user_prompt: str, collection_name: str = "prompts"):
        """
        사용자 프롬프트를 MongoDB에 저장합니다.
        
        :param user_prompt: 사용자 입력 프롬프트
        :param collection_name: 저장할 컬렉션 이름 (기본값: 'prompts')
        """
        if self.db is None:
            print("❌ MongoDB 연결이 없습니다. 프롬프트를 저장할 수 없습니다.")
            return
        try:
            data = {
                "prompt": user_prompt,
                "timestamp": datetime.now()
            }
            result = self.db[collection_name].insert_one(data)
            print(f"✅ 프롬프트 저장 성공 (문서 ID: {result.inserted_id})")
        except Exception as e:
            print(f"❌ 프롬프트 저장 실패: {e}")

    def save_response_to_db(self, collection_name: str, prompt: str, response: str):
        """
        Gemini API의 응답과 프롬프트, 현재 시간을 MongoDB에 저장합니다.
        
        :param collection_name: 저장할 컬렉션 이름
        :param prompt: 사용자 입력 프롬프트 (시스템 역할 포함 가능)
        :param response: Gemini의 응답 텍스트
        """
        if self.db is None:
            print("❌ MongoDB 연결이 없습니다. 응답을 저장할 수 없습니다.")
            return
        try:
            data = {
                "prompt": prompt,
                "response": response,
                "timestamp": datetime.now()
            }
            result = self.db[collection_name].insert_one(data)
            print(f"✅ 데이터 저장 성공 (문서 ID: {result.inserted_id})")
        except Exception as e:
            print(f"❌ 데이터 저장 실패: {e}")

    def close_connection(self):
        """
        Gemini API 연결을 해제하고 MongoDB 연결을 종료합니다.
        """
        genai.configure(api_key=None)
        if self.db_connection:
            self.db_connection.close_connection()
        print("Gemini API 연결이 해제되었습니다.")






if __name__ == "__main__":
    load_dotenv()  # .env 파일 로드
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME") or "gemini_db"

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

    # MongoDB 연결 생성
    db_connection = MongoDBConnection(MONGO_URI, DB_NAME)
    
    # GeminiAPI 인스턴스 생성
    gemini = GeminiAPI(GEMINI_API_KEY, db_connection=db_connection)
    
    # 1. 시스템 역할 설정 (예: 판사 역할)
    gemini.set_role("당신은 판사로 찬반 토론을 진행합니다.")
    
    # 2. 사용자 프롬프트 예시
    user_prompt = "토론 주제에 대해서 간략하게 설명해줘."
    
    # 3. 사용자 프롬프트를 DB에 저장
    gemini.insert_prompt(user_prompt)
    
    # 4. Gemini API를 사용하여 기본 응답 생성
    response_text = gemini.generate_text(user_prompt)
    print("판사 (Gemini API):\n", response_text)
    
    # 5. 생성된 응답을 DB에 저장
    gemini.save_response_to_db("responses", user_prompt, response_text)
    
    # --- 벡터스토어를 이용한 답변 생성 예시 ---
    # VectorStoreHandler 인스턴스 생성 (임베딩 모델 및 청크 설정은 필요에 따라 조정)
    vector_handler = VectorStoreHandler(chunk_size=500, chunk_overlap=50)
    
    # 예시: 토론 주제 관련 자료 (실제 운영 시 크롤링 결과 등으로 대체)
    topic_text = (
        "토론 주제: 인공지능의 윤리적 문제에 대해 다양한 관점이 존재합니다. "
        "찬성 측은 기술 발전과 혁신의 필요성을 강조하며, 반대 측은 개인정보 보호와 사회적 불평등 문제를 지적합니다. "
        "이와 관련해 여러 연구와 사례가 보고되고 있습니다."
    )
    
    # 주제 자료를 벡터스토어에 저장 (FAISS 인스턴스 생성)
    topic_vectorstore = vector_handler.store_topic_material(topic_text)
    
    # 6. 벡터스토어 기반 컨텍스트를 포함한 Gemini API 응답 생성
    response_text_vs = gemini.generate_text_with_vectorstore(user_prompt, topic_vectorstore, k=3, max_tokens=200)
    print("판사 (Gemini API with VectorStore):\n", response_text_vs)
    
    # 7. Gemini API 및 MongoDB 연결 종료
    gemini.close_connection()
