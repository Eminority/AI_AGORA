from crawling import DebateDataProcessor

# 실행 예시
if __name__ == "__main__":
    API_KEY = "AIzaSyBM8Uo3sNxvlxmf-BwTIkVEHLrpdIzSWGg"  # Google Custom Search API 키 입력
    CX = "f69d94a4f70514eea"  # Google 맞춤 검색 엔진 ID 입력

    processor = DebateDataProcessor(API_KEY, CX, max_results=3, headless=False)
    topic = "AI technology"
    
    articles = processor.get_articles(topic)

    # 결과 출력
    for idx, article in enumerate(articles, 1):
        print(f"기사 {idx}:\n{article['content'][:500]}...\n")  # 500자까지만 미리보기 출력

    processor.quit_driver()
