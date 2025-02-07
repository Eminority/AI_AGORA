from vectorstore_module import VectorStoreHandler

# participant 또는 심판으로 들어갈 ai
class Agora_AI:
    def __init__(ai_type:str, ai_instance, vector_handler:VectorStoreHandler=None):
        self.ai_type = ai_type
        self.ai_instance = ai_instance
        self.vector_handler = vector_handler
        self.vectorstore = None
        self.crawled_data = []

    def set_role(role):
        if role == "judge":
            role = "판사 프롬프트"
        elif role == "pos":
            role = "주제에 대하여 찬성하라는 프롬프트"
        elif role == "neg":
            role = "주제에 대하여 반대하라는 프롬프트"
        if self.ai_type == "GEMINI":
            self.ai_instance.set_role(role)

    def crawling(topic:str):
        #주제와 self.role을 기반으로 crawling해서 crawled_data에 집어넣기.
        self.crawled_data.extend(["crawled","data","list"])
        
    def vectorstoring():
        self.vectorstore = self.vector_handler.vectorstoring_from_list(self.crawled_data)

    def generate_text(prompt: str, k:int = 3, max_tokens:int = 200):
        if self.ai_type == "GEMINI":
            return self.ai_instance.generate_text_with_vectorstore(prompt, k=k, max_tokens=max_tokens)
        else :
            return "등록된 형태의 ai가 아닙니다."