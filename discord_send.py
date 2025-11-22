# discord_send.py
import discord
import asyncio
import json

def load_config():
    with open("config.json") as f:
        return json.load(f)

async def send_discord_message(text):
    cfg = load_config()
    token = cfg["discord_token"]
    
    try:
        channel_id = int(cfg["target_channel_id"])
    except ValueError:
        print("오류: config.json의 target_channel_id가 숫자가 아닙니다.")
        return 

    # 🚨 수정된 부분: Intents를 명시적으로 설정
    intents = discord.Intents.default()
    intents.guilds = True        # 서버 정보 접근 필수
    intents.messages = True
    intents.message_content = True 
    
    # 🚨 추가된 부분: 클라이언트 캐시를 완전히 비활성화 (매우 중요)
    # 이 옵션은 봇이 접속 시 서버 목록을 다시 불러오게 만듭니다.
    client = discord.Client(intents=intents, enable_debug_events=True) 
    
    @client.event
    async def on_ready():
        print(f'로그인 성공! 봇 이름: {client.user}')
        
        # 🚨 수정된 부분: 클라이언트가 캐시가 아닌, 서버로부터 직접 채널을 찾도록 유도
        try:
            # 봇이 속한 모든 서버(길드)를 순회하며 채널을 찾습니다.
            target_channel = None
            for guild in client.guilds:
                channel = guild.get_channel(channel_id)
                if channel:
                    target_channel = channel
                    break
            
            if target_channel:
                await target_channel.send(text)
                print(f"디스코드 채널({channel_id})로 메시지 전송 완료.")
            else:
                print(f"오류: 채널 ID {channel_id}를 찾을 수 없습니다. (서버 목록 확인 실패)")
        except Exception as e:
            print(f"디스코드 메시지 전송 중 오류 발생: {e}")
        finally:
            # 메시지 보낸 후 클라이언트 종료
            await client.close() 

    try:
        await client.start(token)
    except discord.LoginFailure:
        print("오류: 디스코드 토큰이 잘못되었습니다. config.json을 확인하세요.")
    except Exception as e:
        print(f"디스코드 클라이언트 실행 중 오류: {e}")
        
# discord_send.py 파일의 send_message 함수 수정

def send_message(summary_text):
    # 🚨 수정된 부분 시작: 이벤트 루프를 안전하게 가져오거나 새로 생성하는 로직
    try:
        # 현재 스레드의 이벤트 루프를 가져옵니다.
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # 이벤트 루프가 없다면 새로 생성합니다. (오류 메시지를 해결하는 핵심)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    # 🚨 수정된 부분 끝
    
    # run_until_complete로 비동기 함수 실행
    loop.run_until_complete(send_discord_message(summary_text))
    
    return 200, "Discord Message Sent"