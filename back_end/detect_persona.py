from langchain_community.retrievers import WikipediaRetriever
from langchain_ollama import ChatOllama  
from langchain.prompts import PromptTemplate
import google.generativeai as genai

class DetectPersona:
    """
    객체 정보를 검색하고 성격을 분석하여 DB에 저장하는 클래스.
    - Wikipedia 또는 GEMINI API를 활용하여 정보 검색
    - 성격 분석을 GEMINI API 또는 Local 모델(Ollama) 중 선택 가능
    - 결과를 MongoDB에 자동 저장
    """

    def __init__(self, db_connection, AI_API_KEY=None):
        self.db = db_connection  
        self.source = "wikipedia"  # 검색 소스: "wikipedia" 또는 "gemini"
        self.local_model = "llama3.2"  # Local 모델 이름
        self.retriever = WikipediaRetriever()

        # try:
        #     self.local_llm = ChatOllama(model=self.local_model)
        #     print(f"✅ Local 모델이 '{self.local_model}'으로 설정되었습니다.")
        # except Exception as e:
        #     print(f"{self.local_model} 을 찾을 수 없습니다. \n {e}")
        # GEMINI API 설정
        if AI_API_KEY:
            genai.configure(api_key=AI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-pro')


    def get_traits(self, object_name: str) -> str:
        """
        객체 정보를 검색하고 성격 분석을 수행.
        - DB에 해당 객체 정보가 존재하면 그대로 반환.
        - 존재하지 않으면 새로 분석 후 DB에 저장.
        """
        # 🔹 기존 데이터 조회
        existing_data = self.db.db["object"].find_one({"name": object_name})
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
            template="Based on the following information, describe the personality traits of {object_name} in only 1 briefly and short sentence words: {context}"
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
        - object_attribute 값에서 `</think>` 이후의 문장만 저장
        """
        if isinstance(attributes, AIMessage):
            attributes = attributes.content  # 🔹 AIMessage 객체에서 content(텍스트)만 추출

        # 🔹 `</think>` 이후의 문장만 저장
        if "</think>" in attributes:
            attributes = attributes.split("</think>", 1)[-1].strip()

        new_profile = {
            "name": name,
            "ai": self.local_model if self.local_model else "GEMINI",
            "object_attribute": attributes,  
            "create_time": datetime.datetime.utcnow()
        }

        profile_id = self.db.insert_data("object", new_profile)
        print(f"✅ 새 프로필이 생성되었습니다! (ID: {profile_id})")
        return new_profile

