import wikipedia
from bs4 import BeautifulSoup

class WikipediaSearcher:
    """
    Wikipedia에서 특정 object에 대한 정보를 검색하여 내용을 가져오는 클래스.
    """
    def __init__(self, language="en"):
        wikipedia.set_lang(language)  # 언어 설정

    def get_page_content(self, object_name):
        """
        Wikipedia에서 object_name과 일치하는 페이지 내용을 가져옴.

        Parameters:
            object_name (str): 검색할 객체 이름
        
        Returns:
            str: Wikipedia 페이지 내용 (실패 시 None)
        """
        try:
            # 🔹 정확한 object_name을 먼저 검색 (auto_suggest=False)
            page = wikipedia.page(object_name, auto_suggest=False)
            return page.content

        except wikipedia.DisambiguationError as e:
            print(f"⚠️ 다의어 발생: {object_name} -> 후보군: {e.options[:5]}")

            # 🔹 후보 목록 중 object_name이 포함된 항목이 있으면 우선 선택
            filtered_options = [opt for opt in e.options if object_name.lower() in opt.lower()]
            if filtered_options:
                print(f"🔍 '{filtered_options[0]}' 페이지를 선택합니다.")
                return wikipedia.page(filtered_options[0]).content

            # 🔹 object_name이 포함되지 않은 경우, 첫 번째 검색 결과를 사용
            print(f"⚠️ '{e.options[0]}' 페이지를 대신 선택합니다.")
            return wikipedia.page(e.options[0]).content

        except wikipedia.PageError:
            print(f"❌ Wikipedia에서 '{object_name}' 페이지를 찾을 수 없습니다.")
            return None
