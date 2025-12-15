# discord_send.py
import discord
import asyncio
import json
import os # 🚨 추가: 파일 경로 및 존재 여부 확인을 위해 os 모듈 임포트

def load_config():
    with open("config.json") as f:
        return json.load(f)

# 🚨 send_discord_message 함수 수정: image_paths 인자를 추가하여 파일 목록을 받습니다.
async def send_discord_message(text, image_paths):
    cfg = load_config()
    token = cfg["discord_token"]
    
    try:
        channel_id = int(cfg["target_channel_id"])
    except ValueError:
        print("오류: config.json의 target_channel_id가 숫자가 아닙니다.")
        return 

    # Intents 설정 (기존과 동일)
    intents = discord.Intents.default()
    intents.guilds = True        
    intents.messages = True
    intents.message_content = True 
    
    # 클라이언트 초기화 (기존과 동일)
    client = discord.Client(intents=intents, enable_debug_events=True) 
    
    @client.event
    async def on_ready():
        print(f'로그인 성공! 봇 이름: {client.user}')
        
        try:
            target_channel = None
            for guild in client.guilds:
                channel = guild.get_channel(channel_id)
                if channel:
                    target_channel = channel
                    break
            
            if target_channel:
                # 🚨 수정된 부분: 이미지 파일 전송 로직 추가 시작
                files_to_send = []
                for path in image_paths:
                    if os.path.exists(path):
                        # 파일 객체를 생성하여 목록에 추가합니다.
                        files_to_send.append(discord.File(path))
                
                # 텍스트 메시지 내용
                message_content = f"**📰 최신 경제 뉴스 요약 (Gemini AI)**\n\n{text}"
                
                # 2. 메시지 전송 (텍스트와 파일 목록)
                if files_to_send:
                    await target_channel.send(
                        content=message_content, 
                        files=files_to_send # 파일 목록 전달
                    )
                    print(f"디스코드 채널({channel_id})로 메시지와 {len(files_to_send)}개 차트 전송 완료.")
                else:
                    # 파일이 없을 경우 텍스트만 보냅니다.
                    await target_channel.send(content=message_content)
                    print(f"디스코드 채널({channel_id})로 텍스트 메시지만 전송 완료.")
                # 🚨 이미지 파일 전송 로직 추가 끝
                    
            else:
                print(f"오류: 채널 ID {channel_id}를 찾을 수 없습니다. (서버 목록 확인 실패)")
        except Exception as e:
            print(f"디스코드 메시지 전송 중 오류 발생: {e}")
        finally:
            # 메시지 보낸 후 클라이언트 종료 (기존과 동일)
            await client.close() 

    try:
        await client.start(token)
    except discord.LoginFailure:
        print("오류: 디스코드 토큰이 잘못되었습니다. config.json을 확인하세요.")
    except Exception as e:
        print(f"디스코드 클라이언트 실행 중 오류: {e}")
        
# 🚨 send_message 함수 수정: image_files 인자를 기본값([])과 함께 받도록 변경
def send_message(summary_text, image_files=[]):
    # 이벤트 루프를 안전하게 가져오거나 새로 생성하는 로직 (기존과 동일)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # 🚨 run_until_complete로 비동기 함수 실행 시 image_files 인자 전달
    loop.run_until_complete(send_discord_message(summary_text, image_files))
    
    return 200, "Discord Message Sent"
