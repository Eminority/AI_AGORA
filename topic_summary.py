import json
from llm_model_pull import OllamaRunner

class DebateLLMProcessor:
    def __init__(self, model_name="mistral"):
        """LLM 모델을 설정하여 주제 분석을 담당하는 클래스"""
        self.model = OllamaRunner()
        self.model.set_model(model_name)

    def generate_summary(self, topic, articles_text):
        """LLM을 사용하여 기사 요약 생성"""
        prompt = f"Summarize the following articles on the topic '{topic}':\n\n" + "\n\n".join(articles_text)
        return self.model.generate_text(prompt)

    def generate_argument(self, topic, stance, articles_text):
        """LLM을 사용하여 찬반 입장 분석"""
        prompt = f"Based on these articles, present a strong {stance} argument on '{topic}':\n\n" + "\n\n".join(articles_text)
        return self.model.generate_text(prompt)

    def process_and_save(self, topic, articles_text):
        """주제 분석 및 JSON 파일 저장"""
        summary = self.generate_summary(topic, articles_text)
        pro_argument = self.generate_argument(topic, "pro", articles_text)
        con_argument = self.generate_argument(topic, "con", articles_text)

        output_data = {
            "topic": topic,
            "summary": summary,
            "pro_argument": pro_argument,
            "con_argument": con_argument
        }

        file_name = f"debate_analysis_{topic.replace(' ', '_')}.json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

        print(f"✅ 분석 결과가 '{file_name}' 파일에 저장되었습니다.")
