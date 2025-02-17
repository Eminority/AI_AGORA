from topic_summary import DebateLLMProcessor
from topic_crawler import NPRCrawler
from llm_translator import OllamaTranslator
import json


# if __name__ == "__main__":
#     topic = input("`토론 주제를 입력하세요: ")
    
#     processor = DebateLLMProcessor(model_name="mistral")  # 사용할 모델 지정
#     processor.run_pipeline(topic)  # 🔹 크롤링 → 요약 → 찬반 분석 → JSON 저장 실행

# # ✅ 실행 예제
# if __name__ == "__main__":
#     topic = input("토론 주제를 입력하세요: ")
#     crawler = NPRCrawler(headless=False)  # GUI 창 띄우기
#     articles = crawler.get_top_articles(topic)

#     print("\n🔍 크롤링된 기사:")
#     for idx, article in enumerate(articles, 1):
#         print(f"\n📌 {idx}. {article['title']}\n{article['content']}...")  

#     crawler.close()

# ✅ 실행 예제
if __name__ == "__main__":
    json_file_path = "debate_gun_control.json"  # 🔹 JSON 파일 경로
    translator = OllamaTranslator()  # 번역기 모듈 초기화

    translated_results = translator.translate_json(json_file_path, target_lang="ko")

    if translated_results:
        print("\n🔍 번역된 결과:")
        print(json.dumps(translated_results, indent=4, ensure_ascii=False))


    # # 🔹 모델 변경 후 번역 테스트
    # translator.set_model("llama3") # set_model()으로도 모델 변경 가능
    # translated_text2 = translator.translate("Translate this sentence into French.", "fr")
    # print(translated_text2)  # 👈 프랑스어 번역된 문장만 출력됨