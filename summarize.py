# summarize.py
import json
from google import genai # 🚨 라이브러리 변경 (openai -> google-genai)
from google.genai.errors import APIError

# 설정 파일 로드 함수
def load_config():
    with open("config.json", 'r', encoding='utf-8') as f:
        return json.load(f)

# API 키 로드 및 Gemini 클라이언트 객체 초기화
try:
    cfg = load_config()
    # 🔑 Gemini 클라이언트 객체 생성 (API 키를 자동으로 환경 변수에서 찾거나 인수로 전달합니다)
    client = genai.Client(api_key=cfg.get("gemini_api_key")) 
except Exception as e:
    print(f"Gemini 클라이언트 초기화 중 오류 발생: {e}")
    client = None

def summarize_news(korean_news, us_news):
    if client is None:
        return "Gemini 클라이언트 오류로 요약할 수 없습니다."

    text = "한국 경제 뉴스:\n" + "\n".join(korean_news) + "\n\n"
    text += "미국 경제 뉴스:\n" + "\n".join(us_news)

    prompt = f"""
    아래 한국/미국 경제 및 주식 뉴스를 핵심 5줄로 요약해줘.

    {text}
    """
    
    # 🚨 수정된 부분: client.models.generate_content 호출로 변경
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', # 🚨 모델 이름 변경 (gpt-4o-mini -> gemini-2.5-flash)
            contents=prompt,
        )
        
        # 응답 결과 접근 방식 변경: .text 속성 사용
        return response.text
        
    except APIError as e:
        print(f"Gemini API 호출 중 오류 발생: {e}")
        return "Gemini API 호출에 실패했습니다."
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
        return "뉴스 요약 중 알 수 없는 오류가 발생했습니다."