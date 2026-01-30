from fastapi import FastAPI, Request
import json
import requests
from datetime import datetime
import os

app = FastAPI()

# 直接寫入 Token
CHANNEL_ACCESS_TOKEN = "Z94rd6FQrOWknL+X7rdJxNbask34AiKOKsC7F3QXWTrtjs3oyKYjSYv+polJX78+PApMyn2tDOl4V2HK45mUsitd/LU4L6/cv6TWlA4lBMQNddi1GO3Wu0Uf4uR/K1DmIpg4N/izXJNuNIrtflwQhAdB04t89/1O/w1cDnyilFU="

TRASH_SCHEDULE = [
    {"start": "2026-01-19", "end": "2026-01-23", "staff": "HAN + YI"},
    {"start": "2026-01-26", "end": "2026-01-30", "staff": "HAN + YA"},
    {"start": "2026-02-02", "end": "2026-02-06", "staff": "YI + YA"},
    {"start": "2026-02-09", "end": "2026-02-13", "staff": "HAN + YI"},
    {"start": "2026-02-16", "end": "2026-02-20", "staff": "HAN + YA"},
    {"start": "2026-02-23", "end": "2026-02-27", "staff": "YI + YA"},
    {"start": "2026-03-02", "end": "2026-03-06", "staff": "HAN + YI"},
    {"start": "2026-03-09", "end": "2026-03-13", "staff": "HAN + YA"},
    {"start": "2026-03-16", "end": "2026-03-20", "staff": "YI + YA"},
    {"start": "2026-03-23", "end": "2026-03-27", "staff": "HAN + YI"},
    {"start": "2026-03-30", "end": "2026-04-03", "staff": "HAN + YA"},
    {"start": "2026-04-06", "end": "2026-04-10", "staff": "YI + YA"}
]

RECURRING_TASKS = [
    {"name": "倒垃圾值日", "rule": "每三個月的1號", "description": "安排下個季度的值日生", "months": [1, 4, 7, 10], "day": 1},
    {"name": "廣告報表", "rule": "每月的1-10號", "description": "完成上個月的成效報表+傳給業者", "range": [1, 10]},
    {"name": "拍攝案件", "rule": "每月的10-15號", "description": "確認下個月的拍攝案件", "range": [10, 15]},
    {"name": "追加廣告", "rule": "每月的10-20號", "description": "確認本月的廣告追加預算", "range": [10, 20]},
    {"name": "億品鍋廣告報表", "rule": "每月的15-25號", "description": "完成億品鍋上個月的成效報表+傳給業者", "range": [15, 25]},
    {"name": "品牌活動", "rule": "每月的15-20號", "description": "確認下個月的活動內容", "range": [15, 20]},
    {"name": "貼文排程", "rule": "每月的25-31號", "description": "提供下個月的貼文排程", "range": [25, 31]},
    {"name": "追加單&網紅表單", "rule": "每月的25-31號", "description": "填寫網紅表單與追加單", "range": [25, 31]}
]

def get_weekly_info():
    today = datetime.now()
    day_num = today.day
    month_num = today.month
    today_str = today.strftime("%Y-%m-%d")
    result = ["【🥜本週工作與提醒】"]
    staff = "查無資料"
    for entry in TRASH_SCHEDULE:
        if entry['start'] <= today_str <= entry['end']:
            staff = entry['staff']
            break
    result.append(f"🗑️ 倒垃圾負責人：{staff}")
    tasks = []
    for task in RECURRING_TASKS:
        is_active = False
        if "range" in task:
            if task["range"][0] <= day_num <= task["range"][1]:
                is_active = True
        elif "months" in task and "day" in task:
            if month_num in task["months"] and day_num == task["day"]:
                is_active = True
        if is_active:
            tasks.append(f"📌 {task['name']}：{task['description']}")
    if tasks:
        result.append("\n【本週待辦事項】")
        result.extend(tasks)
    else:
        result.append("\n本週暫無其他定期待辦事項。")
    return "\n".join(result)

@app.get("/")
async def root():
    return {"status": "Diagnostic Bot is running!"}

@app.post("/callback")
async def callback(request: Request):
    try:
        body = await request.body()
        data = json.loads(body)
        print(f"Received event: {data}") # Render Logs 會顯示
        
        for event in data.get("events", []):
            if event.get("type") == "message" and event.get("message", {}).get("type") == "text":
                text = event["message"]["text"].strip()
                reply_token = event["replyToken"]
                
                if any(k in text for k in ["🥜本周", "🥜本週", "🥜倒垃圾"]):
                    message = get_weekly_info()
                    reply_message(reply_token, message)
                else:
                    # 診斷模式：回覆任何訊息以確認 Webhook 是通的
                    reply_message(reply_token, f"🤖 收到您的訊息：『{text}』\n目前 Webhook 連線正常！請輸入『🥜本周』來查詢工作事項。")
    except Exception as e:
        print(f"Error: {str(e)}")
    return "OK"

def reply_message(reply_token, text):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
