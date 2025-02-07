# participant 또는 심판으로 들어갈 ai
class Agora_AI:
    def __init__(ai_type, api, vectorhandler):
        self.ai_type = ai_type
        self.api = api
        self.vectorhandler = vectorhandler
        self.vectorstore = None
        self.crawled_data = []

    def set_role(role):
        if self.ai_type == "GEMINI":
            self.api.set_role(role)

    def crawling(toipc:str):
        #주제와 self.role을 기반으로 crawling해서 crawled_data에 집어넣기.
        self.crawled_data.extend(["crawled","data","list"])
        
    def vectorstoring():
        self.vectorstore = vector_handler.vectorstoring_from_list(self.crawled_data)

    def generate_text(prompt: str, crawled_text = [], max_tokens = 200):
        if self.ai_type == "GEMINI":
            return self.api.generate_text_with_vectorstore(prompt, crawled_text, k=3, max_tokens=max_tokens)
        else :
            return "등록된 형태의 ai가 아닙니다."