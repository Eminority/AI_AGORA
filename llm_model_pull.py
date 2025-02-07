import json
import requests
import subprocess

class OllamaRunner:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.model_name = None  # 🔹 모델을 바로 지정하지 않음

    def set_model(self, model_name):
        """🔹 동적으로 모델을 설정"""
        self.model_name = model_name

    def is_model_installed(self):
        """현재 설치된 Ollama 모델 목록을 확인하여 해당 모델이 있는지 검사"""
        if not self.model_name:
            print("❌ 모델이 설정되지 않았습니다.")
            return False

        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            return self.model_name in result.stdout
        except FileNotFoundError:
            print("❌ Ollama가 설치되지 않았거나 실행할 수 없습니다.")
            return False

    def pull_model(self):
        """모델이 없으면 다운로드 (URL에서 가져와서 설치)"""
        if not self.model_name:
            print("❌ 모델이 설정되지 않았습니다.")
            return False

        print(f"🔍 '{self.model_name}' 모델 확인 중...")
        if self.is_model_installed():
            print(f"✅ '{self.model_name}' 모델이 이미 설치됨.")
            return True

        print(f"📥 '{self.model_name}' 모델 다운로드 중...")
        url = f"{self.base_url}/api/pull"
        response = requests.post(url, json={"name": self.model_name})
        
        if response.status_code == 200:
            print(f"✅ '{self.model_name}' 다운로드 완료!")
            return True
        else:
            print(f"⚠️ 다운로드 실패: {response.text}")
            return False

    def run_model_interactive(self):
        """Ollama 모델을 터미널에서 직접 실행 ('ollama run <model>')"""
        if not self.pull_model():
            print("❌ 모델 실행 실패!")
            return

        print(f"🚀 '{self.model_name}' 모델을 실행 중... ")
        subprocess.run(["ollama", "run", self.model_name])

    def generate_text(self, prompt):
        """프로그래밍 방식으로 텍스트를 입력하면 Ollama 모델이 응답"""
        if not self.pull_model():
            print("❌ 모델 실행 실패!")
            return "Error: Model could not be loaded"

        url = f"{self.base_url}/api/generate"
        payload = {"model": self.model_name, "prompt": prompt}

        with requests.post(url, json=payload, stream=True) as response:
            if response.status_code != 200:
                return f"⚠️ 오류 발생: {response.text}"

            generated_text = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            generated_text += data["response"] + " "
                    except json.JSONDecodeError:
                        continue  # JSON 파싱 오류 발생 시 무시

            return generated_text.strip()
