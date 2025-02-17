from vectorstore_module import VectorStoreHandler
from crawling import DebateDataProcessor

class Agora_AI:
    def __init__(self, ai_type: str, ai_instance, personality: str = "", vector_handler: VectorStoreHandler = None):
        """
        Args:
            ai_type (str): AI 모델 타입 (예: 'GEMINI', 'ollama' 등).
            ai_instance: 실제 AI 모델 인스턴스(또는 API를 감싸는 래퍼).
            vector_handler (VectorStoreHandler, optional): 벡터 스토어 핸들러.
        """
        self.ai_type = ai_type.lower()
        self.ai_instance = ai_instance
        self.vector_handler = vector_handler if vector_handler is not None else VectorStoreHandler()
        self.personality = personality
        self.vectorstore = None
        self.crawled_data = []

        # 지원하는 AI 모델 리스트
        self.supported_models = {
            "gemini", "ollama",
            "deepseek-r1-distill-llama-70b", "deepseek-r1-distill-qwen-32b",
            "gemma2-9b-it", "llama-3.1-8b-instant", "llama-3.2-1b-preview",
            "llama-3.2-3b-preview", "llama-3.3-70b-specdec", "llama-3.3-70b-versatile",
            "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768",
            "qwen-2.5-32b", "qwen-2.5-coder-32b"
        }

        self.set_personality()

    def set_personality(self):
        if self.ai_instance:
            self.ai_instance.set_personality(self.personality)

    def crawling(self, debate_processor: DebateDataProcessor, topic: str):
        """
        주제를 검색하여 기사를 크롤링하고, 결과를 벡터 스토어에 저장한다.

        Args:
            topic (str): 검색할 토론 주제
        """
        articles = debate_processor.get_articles(topic)
        if not articles:
            print("❌ 크롤링된 데이터가 없습니다.")
            return

        print(f"✅ {len(articles)}개의 기사 크롤링 완료!")
        self.crawled_data.extend(articles)  # 크롤링된 기사 누적

        # 크롤링한 데이터를 벡터 스토어에 저장
        self.vectorstoring()

    def vectorstoring(self):
        """
        현재까지 수집된 기사(self.crawled_data)를 벡터 스토어에 저장한다.
        
        VectorStoreHandler의 vectorstoring 메서드를 통해 벡터화 및 저장을 수행하고,
        그 결과를 self.vectorstore에 할당한다.
        
        Raises:
            ValueError: 
                - vector_handler가 초기화되지 않았을 경우
                - 크롤링된 데이터가 비어 있거나 유효한 기사 내용이 없을 경우
                - 벡터 스토어 생성에 실패했을 경우
        """
        if self.vector_handler is None:
            raise ValueError("VectorStoreHandler가 초기화되지 않았습니다.")

        valid_articles = [
            article for article in self.crawled_data
            if article.get("content", "").strip() and article.get("content", "").strip() != "❌ 본문을 가져오지 못했습니다."
        ]
        if not valid_articles:
            raise ValueError("유효한 기사 내용이 없습니다.")

        self.vectorstore = self.vector_handler.vectorstoring(valid_articles)
        
        if self.vectorstore is None:
            raise ValueError("벡터스토어 생성에 실패했습니다.")

    def generate_text(self, prompt: str, k: int = 3, max_tokens: int = 200):
        """
        주어진 prompt와 벡터 스토어를 활용해 텍스트를 생성한다.

        Args:
            prompt (str): AI 모델에 전달할 프롬프트
            k (int): 벡터 스토어에서 검색할 상위 문서 수
            max_tokens (int): 생성할 텍스트의 최대 토큰 수

        Returns:
            str: 생성된 텍스트. 
        """
        if self.ai_type in self.supported_models:
            return self.ai_instance.generate_text_with_vectorstore(prompt, self.vectorstore, k=k, max_tokens=max_tokens)
        return "등록된 형태의 AI가 아닙니다."
