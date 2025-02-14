from wikipediasearcher import WikipediaSearcher
from llm_model_pull import OllamaRunner

class PersonalityExtractor:
    """
    Wikipedia에서 크롤링한 텍스트를 기반으로,
    LLM(예: Ollama)을 호출하여 대상 object의 인격(특징) 요소를 추출하는 클래스.
    """
    def __init__(self, base_url="http://localhost:11434"):
        self.searcher = WikipediaSearcher()
        self.llm_runner = OllamaRunner(base_url=base_url)  # 🔹 모델을 초기화 시 지정하지 않음

    def set_model(self, model_name):
        """🔹 동적으로 LLM 모델을 설정"""
        self.llm_runner.set_model(model_name)

    def get_personality_traits(self, object_name):
        """
        Wikipedia에서 가져온 데이터를 기반으로 특정 object의 성격을 추출.

        Parameters:
            object_name (str): 예를 들어 "apple"

        Returns:
            str: 추출된 성격 요소 문자열
        """
        content = self.searcher.get_page_content(object_name)
        if not content:
            return "❌ 해당 객체에 대한 정보를 찾을 수 없습니다."

        # 페이지 전체 내용이 너무 길다면, 일부(예: 앞 2000자)를 사용
        # truncated_content = content if len(content) <= 100000 else content[:2000]

        # LLM에게 전달할 프롬프트 구성
        prompt = f"Assuming you are {object_name}, describe your personality. Answer within 300 characters"

        response = self.llm_runner.generate_text(prompt)

        return response

# 사용 예시
from personality_extractor import PersonalityExtractor
# 원하는 object 이름과 사용할 LLM 모델만 지정하면 됩니다.
object_name = "bicycle"
llm_model = "mistral"  # 🔹 사용 가능한 LLM 모델 이름

if __name__ == "__main__":
    extractor = PersonalityExtractor()
    
    # 🔹 모델을 main에서 동적으로 설정
    extractor.set_model(llm_model)
    
    traits = extractor.get_personality_traits(object_name)
    print(f"Extracted personality traits for '{object_name}':")
    print(traits)
