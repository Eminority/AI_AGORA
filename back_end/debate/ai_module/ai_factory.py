from gemini import GeminiAPI

class AI_Factory:
    def __init__(api_keys:dict):
        """
        api 키가 필요한 경우 저장하는 곳
        "GEMINI" : "GEMINI_API_KEY" 같은 형태
        """
        self.api = api

    def create_ai_instance(ai_type: str):
        if ai_type == "GEMINI":
            return GeminiAPI(self.api["GEMINI"])
        # 인공지능 유형에 따라 인스턴스 생성하는 방법을 넣어서 추가
        else:
            return None

