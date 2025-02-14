import google.generativeai as genai

# GeminiAPI: 기존 Gemini API를 사용하며, 벡터스토어 기반 컨텍스트 활용 기능을 추가합니다.
class GeminiAPI:
    def __init__(self, api_key: str):
        """
        Gemini 모델을 초기화할 때, 기본적으로 personality(성격)와 role(역할)을 설정함.
        """
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash') #모델 변경 pro -> 2.0-flash
        # self.personality = personality  # 기본 성격
        # self.role = role  # 역할 설정
        
        # print(f"✅ Gemini 모델이 초기화되었습니다! (성격: {self.personality}, 역할: {self.role})")

    def generate_text(self, user_prompt: str, max_tokens: int) -> str:
        """
        Gemini 모델을 사용하여 텍스트를 생성합니다.
        
        :param user_prompt: 사용자 입력 프롬프트
        :param temperature: 창의성 설정 (0.0~1.0)
        :param max_tokens: 생성할 최대 토큰 수
        :return: 생성된 텍스트
        """
        full_prompt = user_prompt
        if self.personality:
            full_prompt = f"personality:{self.personality}\n{user_prompt}"
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    # "temperature": temperature,
                    "max_output_tokens": max_tokens
                }
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_text_with_vectorstore(self, user_prompt: str, vectorstore, max_tokens: int, k: int = 3) -> str:
        """
        벡터스토어에서 관련 컨텍스트를 검색한 후, 이를 포함하여 Gemini API로 답변을 생성합니다.
        
        :param user_prompt: 사용자 입력 프롬프트
        :param vectorstore: FAISS 벡터스토어 인스턴스 (예: 주제 자료가 저장된 벡터스토어)
        :param k: 유사도 검색 시 반환할 문서 수 (기본값: 3)
        :param temperature: 창의성 설정 (0.0~1.0)
        :param max_tokens: 생성할 최대 토큰 수
        :return: 생성된 텍스트
        """
        try:
            # 벡터스토어에서 유사 문서 검색 (각 문서는 page_content 속성을 가짐)
            search_results = vectorstore.similarity_search(user_prompt, k=k)
            context = "\n".join([doc.page_content for doc in search_results])
        except Exception as e:
            context = ""
            print(f"⚠️ 벡터스토어 검색 실패: {e}")

        if self.personality:
            full_prompt = f"System: {self.personality}\nContext: {context}\nUser: {user_prompt}"
        else:
            full_prompt = f"Context: {context}\nUser: {user_prompt}"
            
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    # "temperature": temperature,
                    "max_output_tokens": max_tokens
                }
            )
            return response.text if response.text else "답변 없음"
        except Exception as e:
            return f"Error: {str(e)}"

    def close_connection(self):
        """
        Gemini API 연결을 해제합니다.
        """
        genai.configure(api_key=None)
        print("❌ Gemini API 연결이 해제되었습니다.")
