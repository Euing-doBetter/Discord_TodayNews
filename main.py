# main.py
from news import fetch_korean_news, fetch_us_news
from summarize import summarize_news
from discord_send import send_message # <-- 모듈 변경
from chart_generator import generate_index_charts

def main():
    kr = fetch_korean_news()
    us = fetch_us_news()

    summary = summarize_news(kr, us)
    status, res = send_message(summary)

    # 🚨 추가: 그래프 생성 및 파일 경로 가져오기
    image_files = generate_index_charts()
    
    # 🚨 send_message에 image_files 인자 전달
    status, res = send_message(summary, image_files)
    
    print("디스코드 전송 상태:", status)
    print(res)

if __name__ == "__main__":
    main()
