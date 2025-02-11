from vectorstore_module import VectorStoreHandler

# participant 또는 심판으로 들어갈 ai
class Agora_AI:
    def __init__(self, ai_type:str, ai_instance, vector_handler:VectorStoreHandler=None):
        self.ai_type = ai_type
        self.ai_instance = ai_instance
        self.vector_handler = vector_handler if vector_handler is not None else VectorStoreHandler()  # 기본 핸들러 설정
        self.vectorstore = None
        self.crawled_data = []

    def set_role(self, role):
        if role == "judge":
            role = "Judge side of the topic"
        elif role == "pos":
            role = "Positive side of the topic"
        elif role == "neg":
            role = "Negative side of the topic"
        if self.ai_type == "GEMINI":
            self.ai_instance.set_role(role)

    def crawling(self, topic:str):
        #주제와 self.role을 기반으로 crawling해서 crawled_data에 집어넣기.
        self.crawled_data.extend(["crawled","data","list"])
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