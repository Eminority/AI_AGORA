import json
from llm_model_pull import OllamaRunner
from topic_crawler import NPRCrawler

class DebateLLMProcessor:
    """
    토론 주제에 대한 정보를 크롤링하고 요약 및 찬반 의견을 생성하는 클래스.
    """

    def __init__(self, model_name="mistral"):
        """
        Ollama 기반의 LLM 모델을 설정합니다.

        :param model_name: 사용할 LLM 모델 이름 (기본값: "mistral")
        """
        self.model_name = model_name
        self.llm = OllamaRunner()  # OllamaRunner 인스턴스 생성
        self.llm.set_model(model_name)  # 모델 설정

    def generate_response(self, prompt):
        """
        LLM을 사용하여 주어진 프롬프트에 대한 응답을 생성.

        :param prompt: LLM에게 보낼 요청 텍스트
        :return: LLM의 응답 텍스트
        """
        return self.llm.generate_text(prompt)

    def summarize_articles(self, topic, articles):
        """
        크롤링한 기사 내용을 요약.

        :param topic: 토론 주제
        :param articles: 기사 본문 리스트
        :return: 요약된 내용
        """
        if not articles:
            return "❌ 기사 요약 실패: 크롤링된 기사가 없습니다."

        combined_text = " ".join(articles[:3])  # 상위 3개 기사 내용을 결합
        prompt = f"Summarize the following text about {topic} in 300 words:\n{combined_text}"
        return self.generate_response(prompt)

    def generate_pros_cons(self, topic, summary):
        """
        토론 주제에 대한 찬성 및 반대 의견을 생성.

        :param topic: 토론 주제
        :param summary: 요약된 기사 내용
        :return: (찬성 의견, 반대 의견)
        """
        pro_prompt = f"Provide a pro argument for {topic} based on the following summary:\n{summary}"
        con_prompt = f"Provide a con argument for {topic} based on the following summary:\n{summary}"
        
        pro_argument = self.generate_response(pro_prompt)
        con_argument = self.generate_response(con_prompt)

        return pro_argument, con_argument

    def process_and_save(self, topic, articles):
        """
        크롤링한 데이터를 요약 및 찬반 의견 생성 후 JSON 파일로 저장.

        :param topic: 토론 주제
        :param articles: 기사 본문 리스트
        """
        # 🔹 기사 데이터 구조 확인 (디버깅 용도)
        print(f"\n🔍 크롤링된 기사 데이터 구조 확인: {articles}\n")

        summary = self.summarize_articles(topic, articles)
        pros, cons = self.generate_pros_cons(topic, summary)

        debate_data = {
            "topic": topic,
            "summary": summary,
            "pros": pros,
            "cons": cons
        }

        # JSON 파일로 저장
        file_name = f"debate_{topic.replace(' ', '_')}.json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(debate_data, f, indent=4, ensure_ascii=False)

        print(f"✅ 토론 데이터가 '{file_name}'에 저장되었습니다.")

    def run_pipeline(self, topic):
        """
        토론 주제에 대한 크롤링 → 요약 → 찬반 의견 생성 → 저장까지 수행.

        :param topic: 토론 주제
        """
        print(f"🔍 '{topic}' 관련 기사를 검색하는 중...")
        
        # 🔹 NPR 기사 크롤링
        crawler = NPRCrawler(headless=True)
        articles = crawler.get_top_articles(topic)
        crawler.close()

        if not articles:
            print("❌ 관련 기사를 찾을 수 없습니다.")
            return

        # 🔹 기사 데이터 구조 확인 (디버깅 용도)
        print(f"\n✅ 크롤링된 기사 개수: {len(articles)}")
        for idx, article in enumerate(articles):
            print(f"{idx+1}. 제목: {article.get('title', '❌ 제목 없음')}")
            print(f"   본문 길이: {len(article.get('content', ''))}자\n")

        # 🔹 기사 본문 리스트 추출 (비어있는 기사 제거)
        articles_text = [article["content"] for article in articles if article["content"].strip()]

        # 🔹 기사 본문이 모두 비어있을 경우 예외 처리
        if not articles_text:
            print("❌ 모든 기사 본문이 비어 있습니다. 다시 시도해주세요.")
            return

        # 🔹 요약 및 찬반 의견 생성 후 저장
        self.process_and_save(topic, articles_text)
