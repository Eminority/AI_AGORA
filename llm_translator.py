import subprocess

class OllamaTranslator:
    """
    Ollama를 subprocess를 사용하여 직접 실행하는 번역기 클래스.
    터미널에서 `ollama run <model>`을 실행하는 것과 같은 방식으로 동작함.
    """
    def __init__(self, model="exaone3.5"):
        """
        Ollama 번역기 초기화.

        :param model: 사용할 Ollama 모델 (예: "mistral", "llama3", "gemma" 등. 기본값: "exaone3.5")
        """
        self.model = model
    
    def pull_model(model_name="exaone3.5"):
        "Ollama 모델 다운로드 "
        try:
            print(f"📥 '{model_name}' 모델 다운로드 중...")
            subprocess.run(["ollama", "pull", model_name], check=True)
            print(f"✅ '{model_name}' 모델 다운로드 완료!")
        except subprocess.CalledProcessError:
            print(f"❌ '{model_name}' 모델 다운로드 실패!")

    def set_model(self, model_name):
        """
        번역에 사용할 Ollama 모델을 변경.
        :param model_name: 새롭게 사용할 모델 이름
        """
        self.model = model_name

    def translate(self, text, target_language="ko"):
        """
        Ollama를 사용하여 텍스트를 번역.

        :param text: 번역할 문장
        :param target_language: 번역할 언어 코드 (예: "en", "ko", "es", "fr" 등)
        :return: 딱 번역된 문장만 반환
        """
        prompt = f"Translate only the following text into {target_language} and return only the translation. Do not add any extra words or explanations: '{text}'"
        command = f'echo "{prompt}" | ollama run {self.model}'
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore")
            return result.stdout.strip() if result.stdout else "⚠️ 번역된 내용이 없습니다."
        except Exception as e:
            return f"⚠️ 예외 발생: {e}"

# ✅ 실행 예제
if __name__ == "__main__":
    translator = OllamaTranslator()  #  model = "" 으로 사용할 모델 지정. 기본값 : exaone3.5
    
    text_to_translate = "Hello, the weather is nice today."
    target_lang = "ko"  # 영어 → 한국어 번역

    translated_text = translator.translate(text_to_translate, target_lang)
    print(translated_text)  # 👈 딱 번역된 문장만 출력됨

    # 🔹 모델 변경 후 번역 테스트
    translator.set_model("llama3") # set_model()으로도 모델 변경 가능
    translated_text2 = translator.translate("Translate this sentence into French.", "fr")
    print(translated_text2)  # 👈 프랑스어 번역된 문장만 출력됨
