import datetime
from langchain_community.retrievers import WikipediaRetriever
from langchain_ollama import ChatOllama  # ✅ 최신 패키지로 변경
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from bson import ObjectId
# from db_module import MongoDBConnection

class DetectPersona:
    """
    객체 정보를 검색하고 성격을 분석하여 DB에 저장하는 클래스.
    - Wikipedia 또는 GEMINI API를 활용하여 정보 검색
    - 성격 분석을 GEMINI API 또는 Local 모델(Ollama) 중 선택 가능
    - 결과를 MongoDB에 자동 저장
    """

    def __init__(self, db_connection, AI_API_KEY=None):
        self.db = db_connection  
        self.source = None  # 검색 소스: "wikipedia" 또는 "gemini"
        self.local_model = None  # Local 모델 이름
        self.retriever = WikipediaRetriever()
        self.gemini_model = None
        self.local_llm = None

        # GEMINI API 설정
        if AI_API_KEY:
            genai.configure(api_key=AI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-pro')

    def select_source(self):
        """ 검색 소스를 선택 (Wikipedia 또는 GEMINI) """
        while True:
            print("\n📌 사용할 검색 소스를 선택하세요:")
            print("[1] Wikipedia 기반 검색")
            print("[2] GEMINI 기반 검색")
            choice = input("입력 (1 또는 2): ").strip()

            if choice == "1":
                self.source = "wikipedia"
                break
            elif choice == "2":
                self.source = "gemini"
                if self.gemini_model is None:
                    print("❌ GEMINI API가 설정되지 않았습니다. Wikipedia를 사용합니다.")
                    self.source = "wikipedia"
                break
            else:
                print("❌ 올바른 입력이 아닙니다. 다시 선택하세요.")

        print(f"✅ 검색 소스가 '{self.source}'로 설정되었습니다.")

    def select_model(self):
        """ 성격 분석을 수행할 모델 선택 (Local LLM 또는 GEMINI) """
        while True:
            print("\n📌 성격 분석을 수행할 모델을 선택하세요:")
            print("[1] Local 모델 사용")
            print("[2] GEMINI 사용")
            choice = input("입력 (1 또는 2): ").strip()

            if choice == "1":
                self._select_local_model()
                break
            elif choice == "2":
                if self.gemini_model is None:
                    print("❌ GEMINI API가 설정되지 않았습니다. Local 모델을 사용하세요.")
                    continue
                print("✅ GEMINI를 사용하여 성격 분석을 수행합니다.")
                break
            else:
                print("❌ 올바른 입력이 아닙니다. 다시 선택하세요.")

    def _select_local_model(self):
        """ 로컬 모델을 직접 입력받아 설정 """
        while True:
            local_model_name = input("\n🔍 사용할 Local LLM 모델의 이름을 입력하세요 (종료하려면 'q' 입력): ").strip()

            if local_model_name.lower() == "q":
                print("🚪 프로그램을 종료합니다.")
                exit()

            try:
                self.local_model = local_model_name
                self.local_llm = ChatOllama(model=self.local_model)
                print(f"✅ Local 모델이 '{self.local_model}'으로 설정되었습니다.")
                break  # 정상적으로 설정되었으면 루프 탈출
            except Exception:
                print(f"❌ '{local_model_name}' 모델을 찾을 수 없습니다. 다시 입력하세요.")

    def get_traits(self, object_name: str):
        """
        객체 정보를 검색하고 성격 분석을 수행.
        - DB에 해당 객체 정보가 존재하면 그대로 반환.
        - 존재하지 않으면 새로 분석 후 DB에 저장.
        """
        # 🔹 기존 데이터 조회
        existing_data = self.db.db["profiles"].find_one({"name": object_name})
        if existing_data:
            print(f"✅ 기존 데이터 발견! {object_name}의 정보를 불러옵니다.")
            return self.convert_objectid(existing_data)

        if self.source is None:
            raise ValueError("⚠️ 먼저 select_source()를 호출하여 검색 소스를 설정하세요.")

        # 🔍 정보 검색 단계
        if self.source == "wikipedia":
            docs = self.retriever.invoke(object_name)  # ✅ 최신 LangChain 메서드 사용
            if not docs:
                return "❌ 해당 객체에 대한 정보를 찾을 수 없습니다."
            context = docs[0].page_content
        else:  # GEMINI를 검색용으로 사용
            if self.gemini_model:
                prompt = f"Provide key personality traits for {object_name}."
                response = self.gemini_model.generate_content(prompt)
                context = response.text if response else "❌ 정보를 가져올 수 없습니다."
            else:
                return "❌ GEMINI 모델이 설정되지 않았습니다."

        # 🔍 성격 분석 (Local LLM 또는 GEMINI)
        prompt_template = PromptTemplate(
            input_variables=["object_name", "context"],
            template="Based on the following information, describe the personality traits of {object_name} in under 300 words: {context}"
        )
        final_prompt = prompt_template.format(object_name=object_name, context=context)

        if self.local_model:  # Local 모델 사용
            traits = self.local_llm.invoke(final_prompt)  # ✅ 최신 메서드 사용
        else:  # GEMINI 사용
            if self.gemini_model:
                response = self.gemini_model.generate_content(final_prompt)
                traits = response.text if response else "❌ 성격 분석 실패."
            else:
                return "❌ GEMINI 모델이 설정되지 않았습니다."

        # 🔹 DB 저장
        return self.save_to_db(object_name, traits)

    def save_to_db(self, name, attributes):
        """
        분석된 객체 정보를 DB에 저장.
        """
        new_profile = {
            "name": name,
            "object_attribute": attributes,
            "create_time": datetime.datetime.utcnow().isoformat()  # ✅ JSON 직렬화 가능하도록 변환
        }

        profile_id = self.db.insert_data("object", new_profile)
        new_profile["_id"] = str(profile_id)  # ✅ ObjectId를 문자열로 변환

        print(f"✅ 새 프로필이 생성되었습니다! (ID: {profile_id})")
        return new_profile
