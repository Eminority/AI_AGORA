from .gemini import GeminiAPI
from .ollama import OllamaRunner
from .groq import GroqAPI
from .ai_instance import AI_Instance
class AI_Factory:
    def __init__(self, api_keys:dict):
        """
        api 키가 필요한 경우 저장하는 곳
        "GEMINI" : "GEMINI_API_KEY" 같은 형태
        """
        self.api = api_keys
        print(self.api)

    def create_ai_instance(self, ai_type: str) -> AI_Instance:
        
        #로컬 기반 모델
        #ollma - mixtral 로컬 보델
        if ai_type == "ollama":
            model_name = 'mixtral'
            return OllamaRunner(model_name=model_name)
        
        #GEMINI API KEY 기반 모델
        elif ai_type == "GEMINI":
            return GeminiAPI(self.api["GEMINI"])

        #Groq API 기반 모델
        elif ai_type == "deepseek-r1-distill-llama-70b":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "deepseek-r1-distill-qwen-32b":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "gemma2-9b-it":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "llama-3.1-8b-instant":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "llama-3.2-1b-preview":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "llama-3.2-3b-preview":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "llama-3.3-70b-specdec":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "llama-3.3-70b-versatile":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "llama3-70b-8192":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "llama3-8b-8192":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "mixtral-8x7b-32768":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "qwen-2.5-32b":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)
        
        elif ai_type == "qwen-2.5-coder-32b":
            model_name = ai_type
            return GroqAPI(self.api["GROQ"], model_name=model_name)

        # 인공지능 유형에 따라 인스턴스 생성하는 방법을 넣어서 추가
        else:
            return None

