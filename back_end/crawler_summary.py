import json
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)


class DebateDataProcessor:
    """
    토론 주제에 대한 크롤링 및 요약을 수행하는 클래스.

    Attributes:
        driver (webdriver.Chrome): Selenium WebDriver 인스턴스.
        crawled_data (list): 크롤링된 기사 데이터가 저장될 리스트.
    """

    def __init__(self, headless=True):
        """
        초기화 메서드. WebDriver를 설정하고, 크롤링된 데이터를 저장할 리스트를 초기화한다.
        
        Args:
            headless (bool): 브라우저 창을 표시하지 않고(headless 모드) 실행할지 여부.
        """
        self.driver = self._init_driver(headless)
        self.crawled_data = []

    def _init_driver(self, headless):
        """
        Selenium WebDriver를 초기화한다.

        Args:
            headless (bool): 브라우저 창을 표시하지 않고(headless 모드) 실행할지 여부.

        Returns:
            webdriver.Chrome: 설정된 WebDriver 인스턴스.
        """
        logging.info("Initializing Chrome WebDriver...")

        options = webdriver.ChromeOptions()
        # 불필요한 로그를 최소화하기 위한 설정
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--log-level=3")

        # headless 모드 설정
        if headless:
            options.add_argument("--headless")

        # 기타 옵션 설정
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-software-rasterizer")

        service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Chrome WebDriver initialized.")
        return driver

    def search_articles(self, query, max_results=3):
        """
        특정 주제(query)에 대한 NPR 기사 URL을 검색한다.

        Args:
            query (str): 검색어(주제).
            max_results (int): 가져올 최대 기사 수.

        Returns:
            list: 검색된 기사 URL 리스트.
        """
        logging.info(f"Searching articles on NPR for query: '{query}'")
        search_url = f"https://www.npr.org/search?query={query.replace(' ', '+')}"
        
        self.driver.get(search_url)
        time.sleep(3)  # 페이지 로딩 대기
        
        articles = self.driver.find_elements(By.CSS_SELECTOR, "article h2 a")
        if not articles:
            logging.warning("No articles found for the query.")
            return []

        # 최대 max_results개까지만 추출
        article_links = [a.get_attribute("href") for a in articles[:max_results]]

        # NPR 기사 URL만 필터링
        valid_links = [link for link in article_links if link.startswith("https://www.npr.org/")]
        if not valid_links:
            logging.warning("No valid NPR article links found.")
            return []

        logging.info(f"Found {len(valid_links)} article(s): {valid_links}")
        return valid_links

    def _get_article_content(self, url):
        """
        단일 기사 URL에서 제목과 본문을 크롤링한다.

        Args:
            url (str): 기사 URL.

        Returns:
            dict: 기사 정보(제목, 본문, URL).
        """
        logging.info(f"Fetching article content from: {url}")
        self.driver.get(url)
        time.sleep(3)  # 페이지 로딩 대기

        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # 제목 추출
        title_element = soup.find("h1")
        title = title_element.text.strip() if title_element else "제목 없음"

        # 본문 추출 (storytext가 없을 경우 transcript로 대체)
        content_elements = soup.select("div[data-testid='storytext'] p")
        if not content_elements:
            content_elements = soup.select("div.transcript p")

        if content_elements:
            content = "\n".join([p.text.strip() for p in content_elements])
        else:
            content = ""

        if not content:
            logging.warning("No article content found.")
            content = "❌ 본문을 가져오지 못했습니다."

        return {"title": title, "content": content, "url": url}

    def get_articles(self, topic, num_articles=3):
        """
        주제와 관련된 기사들을 검색 및 크롤링한다.

        Args:
            topic (str): 검색 주제(키워드).
            num_articles (int): 가져올 기사 수.

        Returns:
            list: [{"title": str, "content": str, "url": str}, ...] 형식의 기사 정보 리스트.
        """
        logging.info(f"Starting to crawl articles for topic: '{topic}'")
        article_links = self.search_articles(topic, max_results=num_articles)

        if not article_links:
            logging.warning("No article links to crawl.")
            return []

        articles_data = []
        for link in article_links:
            article_info = self._get_article_content(link)
            # 본문 데이터를 정상적으로 가져오지 못했다면 제외
            if article_info["content"] != "❌ 본문을 가져오지 못했습니다.":
                articles_data.append(article_info)

        logging.info(f"Successfully fetched {len(articles_data)} article(s) with valid content.")
        return articles_data

    def quit_driver(self):
        """
        WebDriver를 종료한다.
        """
        if self.driver:
            logging.info("Quitting Chrome WebDriver.")
            self.driver.quit()
            self.driver = None