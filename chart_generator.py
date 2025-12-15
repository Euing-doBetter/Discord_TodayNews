
# chart_generator.py 파일 최상단에 추가
import matplotlib
matplotlib.use('Agg') # 🚨 백엔드를 'Agg'로 설정하여 Tcl/Tk 의존성 제거
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import date, timedelta

# 지수 심볼 정의
INDEX_SYMBOLS = {
    "KR_KOSPI": "^KS11",  # 코스피
    "KR_KOSDAQ": "^KQ11", # 코스닥
    "US_SP500": "^GSPC",  # S&P 500
    "US_NASDAQ": "^IXIC", # 나스닥
}

# 차트 파일 저장 경로 정의
KR_CHART_PATH = "C:/Users/euing/Documents/vscode/Discord_news/chartpng/kr_index_chart.png"
US_CHART_PATH = "C:/Users/euing/Documents/vscode/Discord_news/chartpng/us_index_chart.png"

def generate_index_charts():
    """
    야후 파이낸스에서 지수 데이터를 가져와 두 개의 차트 파일을 생성합니다.
    생성된 파일 경로 리스트를 반환합니다.
    """
    
    # 30일치 데이터 기간 설정
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    try:
        # 1. 데이터 가져오기
        kr_symbols = [INDEX_SYMBOLS["KR_KOSPI"], INDEX_SYMBOLS["KR_KOSDAQ"]]
        us_symbols = [INDEX_SYMBOLS["US_SP500"], INDEX_SYMBOLS["US_NASDAQ"]]
        
        # 한국 데이터 (yfinance는 KR 시장 마감 후 데이터가 업데이트되므로 조금 늦을 수 있습니다)
        kr_data = yf.download(kr_symbols, start=start_date, end=end_date)['Close']
        # 미국 데이터
        us_data = yf.download(us_symbols, start=start_date, end=end_date)['Close']

        # --- 한국 지수 차트 생성 및 저장 ---
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(10, 5))
        
        kr_data[INDEX_SYMBOLS["KR_KOSPI"]].plot(ax=ax, label='KOSPI', color='blue')
        kr_data[INDEX_SYMBOLS["KR_KOSDAQ"]].plot(ax=ax, label='KOSDAQ', color='orange')
        
        ax.set_title('Past 30 Days: KOSPI vs KOSDAQ', fontsize=15)
        ax.set_xlabel('Date')
        ax.set_ylabel('Index Value')
        ax.legend()
        plt.tight_layout()
        plt.savefig(KR_CHART_PATH) # 파일 저장
        plt.close(fig) # 메모리 해제
        
        # --- 미국 지수 차트 생성 및 저장 ---
        fig, ax = plt.subplots(figsize=(10, 5))
        
        us_data[INDEX_SYMBOLS["US_SP500"]].plot(ax=ax, label='S&P 500', color='green')
        us_data[INDEX_SYMBOLS["US_NASDAQ"]].plot(ax=ax, label='NASDAQ', color='red')
        
        ax.set_title('Past 30 Days: S&P 500 vs NASDAQ', fontsize=15)
        ax.set_xlabel('Date')
        ax.set_ylabel('Index Value')
        ax.legend()
        plt.tight_layout()
        plt.savefig(US_CHART_PATH) # 파일 저장
        plt.close(fig) # 메모리 해제

        return [KR_CHART_PATH, US_CHART_PATH]
        
    except Exception as e:
        print(f"차트 생성 중 오류 발생: {e}")
        return []

if __name__ == '__main__':
    # 테스트를 위한 실행 코드
    files = generate_index_charts()
    print(f"생성된 파일: {files}")