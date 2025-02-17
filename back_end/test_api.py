import os
import json
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def load_api_keys():
    """
    환경 변수에서 AI API 키를 로드하는 공통 함수.
    """
    api_key_json = os.getenv("AI_API_KEY")
    
    # 환경 변수 값 출력 (디버깅용)
    print(f"🔍 [DEBUG] AI_API_KEY 환경 변수 값: {api_key_json}")

    if api_key_json:
        try:
            api_keys = json.loads(api_key_json)  # JSON 변환
            print(f"✅ [DEBUG] 변환된 API 키 딕셔너리: {api_keys}")  # 디버깅 출력
            return api_keys
        except json.JSONDecodeError:
            raise ValueError("환경 변수 'AI_API_KEY'가 올바른 JSON 형식이 아닙니다. .env 파일을 확인하세요.")
    else:
        raise ValueError("환경 변수 'AI_API_KEY'가 설정되지 않았습니다.")

class DebateDataProcessor:
    def __init__(self, max_results=5, headless=True):
        api_keys = load_api_keys()  # 공통 API 키 로드 함수 사용
        self.api_key = api_keys.get("GSE")

        if not self.api_key:
            print(f"❌ [DEBUG] AI_API_KEY에서 'GSE' 키가 없음: {api_keys}")  # 디버깅
            raise KeyError("환경 변수에서 'GSE' 키를 찾을 수 없습니다. .env 파일을 확인하세요.")

        self.cx = os.getenv("CX")
        if not self.cx:
            raise ValueError("환경 변수에서 'CX' 값을 찾을 수 없습니다. .env 파일을 확인하세요.")

        print(f"✅ Google Custom Search API 키 로드 완료: {self.api_key}")
        print(f"✅ Google Custom Search CX ID 로드 완료: {self.cx}")
