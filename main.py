from fastapi import FastAPI, Request
import json
import requests
import os

app = FastAPI()

# 使用您提供的最新 Token
CHANNEL_ACCESS_TOKEN = "772eYoivPc43abwMMAe3IvjMFegB5JlFmUkIg+oj5Ydjfu1KT2tRAwlKCle+XmqlPApMyn2tDOl4V2HK45mUsitd/LU4L6/cv6TWlA4lBMQeuuLHiuECcqtNYqvFkfS+haD1lKSXePENi9Kp1HqyIQdB04t89/1O/w1cDnyilFU="

@app.get("/")
async def root():
    return {"status": "Super Simple Bot is running!"}

@app.post("/callback")
async def callback(request: Request):
    try:
        body = await request.body()
        data = json.loads(body)
        print("DEBUG: Received Data:", json.dumps(data))
        
        for event in data.get("events", []):
            reply_token = event.get("replyToken")
            if reply_token:
                print(f"DEBUG: Attempting to reply to token: {reply_token}")
                reply_message(reply_token, "✅ 系統測試：我收到您的訊息了！這代表連線與 Token 都是正確的。")
    except Exception as e:
        print(f"DEBUG: Error in callback: {str(e)}")
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
    response = requests.post(url, headers=headers, json=payload)
    print(f"DEBUG: LINE API Status: {response.status_code}")
    print(f"DEBUG: LINE API Response: {response.text}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
