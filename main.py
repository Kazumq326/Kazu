from fastapi import FastAPI
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import feedparser

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "LINE News Bot is running"}

@app.get("/send-now")
def send_now():
    result = push_line_news()
    return {"message": "ニュースを今すぐ配信しました", "result": result}

def fetch_news():
    # GoogleニュースのAIトピックRSS
    feed_url = "https://news.google.com/rss/search?q=AI&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(feed_url)
    message = "【朝の最新AIニュース】\n"
    for i, entry in enumerate(feed.entries[:5], 1):  # 最新5件
        message += f"{i}. {entry.title}\n   {entry.link}\n"
    return message

def push_line_news():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer wFTPa6Rq+zkjUrE/folctMILqOYbFHLdDAFpebuUrFOwMXeQ6zznxEiBzeeKw88qw0V2nxJHoHd/RavbWL0/1S6LZR1kBRZvL2KUrqZbe4jcrEGq/VnkNuka/blHBoFv0RLPVgv+vQwyi7g1ypwoxQdB04t89/1O/w1cDnyilFU="
    }
    body = {
        "to": "U96ff579ac264705d5b40723e395859b0",
        "messages": [{"type": "text", "text": fetch_news()}]
    }
    response = requests.post("https://api.line.me/v2/bot/message/push", json=body, headers=headers)
    print(response.status_code, response.text)  # ← ここでレスポンスを確認
    return {"status_code": response.status_code, "response": response.text}

def start_scheduler():
    print("スケジューラーを開始します...")
    scheduler = BackgroundScheduler(timezone="Asia/Tokyo")
    scheduler.add_job(push_line_news, 'cron', hour=7, minute=0)
    scheduler.start()
    print("スケジューラーが開始されました。毎朝7時に配信されます。")

start_scheduler()


    


# FastAPIの後ろにこれつけるとスクリプトが止まら




