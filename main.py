# main.py
from news import fetch_korean_news, fetch_us_news
from summarize import summarize_news
from discord_send import send_message # <-- 모듈 변경

def main():
    kr = fetch_korean_news()
    us = fetch_us_news()

    summary = summarize_news(kr, us)
    status, res = send_message(summary)

    print("디스코드 전송 상태:", status)
    print(res)

if __name__ == "__main__":
    main()