from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

class NPRCrawler:
    """NPR에서 특정 주제의 기사 검색 및 본문 크롤링하는 클래스"""

    def __init__(self, headless=True):
        """Selenium 드라이버 초기화"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")  # GUI 없이 실행
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def search_articles(self, query, num_results=3):
        """ 검색어를 입력하고 상위 기사 URL을 가져오는 함수 """
        search_url = f"https://www.npr.org/search?query={query.replace(' ', '+')}"
        self.driver.get(search_url)
        time.sleep(3)

        # 기사 링크 추출
        articles = self.driver.find_elements(By.CSS_SELECTOR, "h2.title a")
        article_links = [article.get_attribute("href") for article in articles[:num_results]]

        return article_links

    def get_article_content(self, url):
        """ 기사 URL에서 제목과 본문을 크롤링하는 함수 """
        self.driver.get(url)
        time.sleep(3)  # 페이지 로딩 대기

        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # ✅ 기사 제목 가져오기
        title_element = soup.find("h1")
        title = title_element.text.strip() if title_element else "제목 없음"

        # ✅ 본문 가져오기
        content_elements = soup.select("div[data-testid='storytext'] p")  # 기본 본문
        if not content_elements:
            content_elements = soup.select("div.transcript p")  # Transcript 내 본문 텍스트

        content = "\n".join([p.text.strip() for p in content_elements])

        if not content:
            content = "❌ 본문을 가져오지 못했습니다."

        return {
            "title": title,
            "content": content,
            "url": url
        }

    def get_top_articles(self, topic, num_articles=3):
        """ 주제에 대한 상위 기사들을 크롤링하여 반환 """
        article_links = self.search_articles(topic, num_articles)
        articles = [self.get_article_content(link) for link in article_links]
        return [article for article in articles if article]

    def close(self):
        """ 드라이버 종료 """
        self.driver.quit()


# ✅ 실행 예제
if __name__ == "__main__":
    topic = input("토론 주제를 입력하세요: ")
    crawler = NPRCrawler(headless=False)  # GUI 창 띄우기
    articles = crawler.get_top_articles(topic)

    print("\n🔍 크롤링된 기사:")
    for idx, article in enumerate(articles, 1):
        print(f"\n📌 {idx}. {article['title']}\n{article['content'][:500]}...")  # 긴 본문은 앞부분만 표시

    crawler.close()
