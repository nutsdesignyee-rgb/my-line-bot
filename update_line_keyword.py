import requests
import json
from datetime import datetime

# 設定資訊
ACCESS_TOKEN = "Z94rd6FQrOWknL+X7rdJxNbask34AiKOKsC7F3QXWTrtjs3oyKYjSYv+polJX78+PApMyn2tDOl4V2HK45mUsitd/LU4L6/cv6TWlA4lBMQNddi1GO3Wu0Uf4uR/K1DmIpg4N/izXJNuNIrtflwQhAdB04t89/1O/w1cDnyilFU="
LINE_GROUP_ID = "C1548151f5ef184ec0bfe83c666301863" # 請替換為您的 LINE 群組 ID
KEYWORD = "🥜倒垃圾"

def get_staff_info():
    try:
        with open('/home/ubuntu/trash_schedule.json', 'r') as f:
            schedule = json.load(f)
        
        today = datetime.now().strftime("%Y-%m-%d")
        for entry in schedule:
            if entry['start'] <= today <= entry['end']:
                return f"【本週倒垃圾負責人】\n日期：{entry['start']} - {entry['end']}\n負責人：{entry['staff']}\n\n請記得準時倒垃圾喔！"
        return "目前班表查無資料，請聯繫管理員更新班表。"
    except Exception as e:
        return f"查詢失敗：{str(e)}"

def push_message(to, text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    payload = {
        "to": to,
        "messages": [{"type": "text", "text": text}]
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Push message status: {response.status_code}")
    print(f"Push message response: {response.text}")

if __name__ == "__main__":
    message_content = get_staff_info()
    if LINE_GROUP_ID == "Cxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx": # 檢查是否已替換為實際群組 ID
        print("錯誤：請在 update_line_keyword.py 中設定正確的 LINE_GROUP_ID。")
    else:
        push_message(LINE_GROUP_ID, message_content)
