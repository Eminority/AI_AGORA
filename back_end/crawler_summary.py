import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class DebateDataProcessor:
    """
    토론 주제에 대한 크롤링 및 요약을 수행하는 클래스.
    """

    def __init__(self, headless=True):
        self.driver = self._init_driver(headless)
        self.crawled_data = []  # 크롤링된 데이터 저장

    def _init_driver(self, headless):
        """Selenium WebDriver 초기화"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-software-rasterizer")  # WebGL 오류 해결
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def search_articles(self, query, num_results=3):
        """ 특정 주제에 대한 기사 URL을 검색 """
        search_url = f"https://www.npr.org/search?query={query.replace(' ', '+')}"
        self.driver.get(search_url)
        time.sleep(3)

        articles = self.driver.find_elements(By.CSS_SELECTOR, "article h2 a")

        article_links = [article.get_attribute("href") for article in articles[:num_results]]
        article_links = [link for link in article_links if link.startswith("https://www.npr.org/")]

        if not article_links:
            print("❌ 검색 결과가 없습니다.")
        return article_links

    def get_article_content(self, url):
        """ 기사 URL에서 제목과 본문을 크롤링 """
        self.driver.get(url)
        time.sleep(3)  # 페이지 로딩 대기

        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        title_element = soup.find("h1")
        title = title_element.text.strip() if title_element else "제목 없음"

        content_elements = soup.select("div[data-testid='storytext'] p")  
        if not content_elements:
            content_elements = soup.select("div.transcript p")

        content = "\n".join([p.text.strip() for p in content_elements]) if content_elements else "❌ 본문을 가져오지 못했습니다."

        return {"title": title, "content": content, "url": url}

    def get_articles(self, topic, num_articles=3):
        """ 주제와 관련된 기사들을 크롤링 """
        print(f"🔍 '{topic}'에 대한 기사 검색 중...")
        article_links = self.search_articles(topic, num_articles)

        if not article_links:
            print("❌ 검색된 기사가 없습니다.")
            return []

        print(f"✅ {len(article_links)}개의 기사 발견! 크롤링 시작...")
        articles = [self.get_article_content(link) for link in article_links]

        # 본문이 비어 있는 기사 제외
        return [article for article in articles if article["content"] != "❌ 본문을 가져오지 못했습니다."]

    # def generate_summary(self, topic, articles):
    #     """ 크롤링한 기사 내용을 요약 """
    #     if not articles:
    #         return "기사 요약 실패: 크롤링된 기사가 없습니다."

    #     combined_text = " ".join([article["content"] for article in articles[:3]])
    #     prompt = f"Summarize the following text about {topic} in 300 words:\n{combined_text}"

    #     return self.llm.generate_text(prompt)




#     def generate_pos_neg(self, topic, summary):
#         """찬성 및 반대 의견 생성"""
#         pos_prompt = f"Provide a pro argument for {topic} based on the following summary:\n{summary}"
#         neg_prompt = f"Provide a con argument for {topic} based on the following summary:\n{summary}"

#         pos = self.llm.generate_text(pos_prompt) or "No pro argument generated."
#         neg = self.llm.generate_text(neg_prompt) or "No con argument generated."

#         return pos, neg

#     def run_pipeline(self, topic):
#         """주제를 기반으로 크롤링 후 요약"""
#         articles = self.get_articles(topic)
#         if not articles:
#             return None

#         summary = self.generate_summary(topic, articles)
#         pos, neg = self.generate_pos_neg(topic, summary)

#         return {
#             "topic": topic,
#             "summary": summary,
#             "pos": pos,
#             "neg": neg,
#             "articles": articles
#         }


#     def close(self):
#         """ WebDriver 종료 """
#         self.driver.quit()


# # ✅ 실행 예제
# if __name__ == "__main__":
#     test_topic = input("토론 주제를 입력하세요: ")
#     processor = DebateDataProcessor(model_name="mistral", headless=False)  # GUI 창 띄우기

#     try:
#         print(f"\n🔍 [1] '{test_topic}'에 대한 기사 크롤링 중...")
#         crawled_data = processor.run_pipeline(test_topic)

#         if crawled_data:
#             print("\n✅ [2] 크롤링 성공! 데이터 출력:")
#             print(json.dumps(crawled_data, indent=4, ensure_ascii=False))
#         else:
#             print("\n❌ [2] 크롤링 실패: 기사 데이터를 가져오지 못했습니다.")

#     except Exception as e:
#         print(f"\n❌ 오류 발생: {str(e)}")

#     finally:
#         processor.close()  # WebDriver 종료
