from .gemini import GeminiAPI
from .ollama import OllamaRunner
class AI_Factory:
    def __init__(self, api_keys:dict):
        """
        api 키가 필요한 경우 저장하는 곳
        "GEMINI" : "GEMINI_API_KEY" 같은 형태
        """
        self.api = api_keys

    def create_ai_instance(self, ai_type: str):
        if ai_type == "GEMINI":
            return GeminiAPI(self.api["GEMINI"])
        elif ai_type == "ollama":
            model_name = 'mistral'
            return OllamaRunner(model_name=model_name)

        # 인공지능 유형에 따라 인스턴스 생성하는 방법을 넣어서 추가
        else:
            return None

