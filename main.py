from fastapi import FastAPI, Request
import json
import requests
from datetime import datetime
import os

app = FastAPI()

# 直接寫入 Token 確保連線
CHANNEL_ACCESS_TOKEN = "Z94rd6FQrOWknL+X7rdJxNbask34AiKOKsC7F3QXWTrtjs3oyKYjSYv+polJX78+PApMyn2tDOl4V2HK45mUsitd/LU4L6/cv6TWlA4lBMQNddi1GO3Wu0Uf4uR/K1DmIpg4N/izXJNuNIrtflwQhAdB04t89/1O/w1cDnyilFU="

def get_weekly_info():
    try:
        file_path = 'trash_schedule.json'
        if not os.path.exists(file_path):
            return "⚠️ 找不到班表檔案，請檢查 GitHub 上的 trash_schedule.json"
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        today = datetime.now()
        day_num = today.day
        month_num = today.month
        today_str = today.strftime("%Y-%m-%d")
        
        result = ["【🥜本週工作與提醒】"]
        
        # 1. 處理倒垃圾班表 (增加多重結構相容性)
        staff = "查無資料"
        trash_list = []
        if isinstance(data, dict):
            trash_list = data.get("trash_schedule", [])
        elif isinstance(data, list):
            trash_list = data
            
        for entry in trash_list:
            if entry.get('start') <= today_str <= entry.get('end'):
                staff = entry.get('staff')
                break
        result.append(f"🗑️ 倒垃圾負責人：{staff}")
        
        # 2. 處理定期事項
        tasks = []
        recurring_tasks = data.get("recurring_tasks", []) if isinstance(data, dict) else []
        
        for task in recurring_tasks:
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
    except Exception as e:
        return f"❌ 系統讀取錯誤：{str(e)}\n請確認 JSON 格式是否正確。"

@app.get("/")
async def root():
    return {"status": "Bot is running!"}

@app.post("/callback")
async def callback(request: Request):
    try:
        body = await request.body()
        data = json.loads(body)
        
        for event in data.get("events", []):
            if event.get("type") == "message" and event.get("message", {}).get("type") == "text":
                text = event["message"]["text"].strip()
                reply_token = event["replyToken"]
                
                # 支援多種關鍵字觸發
                if any(k in text for k in ["🥜本周", "🥜本週", "🥜倒垃圾"]):
                    message = get_weekly_info()
                    reply_message(reply_token, message)
    except Exception:
        pass
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
