from vectorstore_module import VectorStoreHandler
from crawler_summary import DebateDataProcessor
# participant 또는 심판으로 들어갈 ai
class Agora_AI:
    def __init__(self, ai_type:str, ai_instance, vector_handler:VectorStoreHandler=None):
        self.ai_type = ai_type
        self.ai_instance = ai_instance
        self.vector_handler = vector_handler if vector_handler is not None else VectorStoreHandler()  # 기본 핸들러 설정
        self.vectorstore = None
        self.crawled_data = []
        self.debate_processor = DebateDataProcessor()  


    def set_role(self, role):
        if role == "judge":
            role = "Judge side of the topic"
        elif role == "pos":
            role = "Positive side of the topic"
        elif role == "neg":
            role = "Negative side of the topic"
        if self.ai_type == "GEMINI":
            self.ai_instance.set_role(role)

    def crawling(self, topic: str):
        """ 주제와 관련된 기사들을 크롤링하여 crawled_data에 저장 """
        articles = self.debate_processor.get_articles(topic)  # DebateDataProcessor의 get_articles 호출
        
        if not articles:
            print("❌ 크롤링된 데이터가 없습니다.")
            return

        print(f"✅ {len(articles)}개의 기사 크롤링 완료!")
        
        # 크롤링된 데이터를 crawled_data에 추가
        self.crawled_data.extend(articles)
        
        # 벡터 저장 함수 호출
        self.vectorstoring()
        
    def vectorstoring(self):
        if self.vector_handler is None:
            raise ValueError("VectorStoreHandler가 초기화되지 않았습니다. Agora_AI 인스턴스를 생성할 때 vector_handler를 전달했는지 확인하세요.")

        self.vectorstore = self.vector_handler.vectorstoring(self.crawled_data)

        if self.vectorstore is None:
            raise ValueError("벡터스토어 생성에 실패했습니다.")
    def generate_text(self, prompt: str, k:int = 3, max_tokens:int = 200):
        if self.ai_type == "GEMINI":
            return self.ai_instance.generate_text_with_vectorstore(prompt, self.vectorstore, k=k, max_tokens=max_tokens)
        elif self.ai_type == "ollama":
            return self.ai_instance.generate_text_with_vectorstore(prompt, self.vectorstore, k=k, max_tokens=max_tokens)
        else :
            return "등록된 형태의 ai가 아닙니다."