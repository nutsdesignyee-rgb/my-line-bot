import requests
import json
from datetime import datetime

# 設定您的 LINE Channel Access Token 和群組 ID
CHANNEL_ACCESS_TOKEN = "Z94rd6FQrOWknL+X7rdJxNbask34AiKOKsC7F3QXWTrtjs3oyKYjSYv+polJX78+PApMyn2tDOl4V2HK45mUsitd/LU4L6/cv6TWlA4lBMQNddi1GO3Wu0Uf4uR/K1DmIpg4N/izXJNuNIrtflwQhAdB04t89/1O/w1cDnyilFU=" # 請替換為您的 Channel Access Token
LINE_GROUP_ID = "C1548151f5ef184ec0bfe83c666301863" # 請替換為您的 LINE 群組 ID

def get_weekly_tasks_info():
    # 這裡可以根據實際需求，動態生成或從文件讀取本週待辦事項
    # 為了簡化，這裡先使用一個範例訊息
    today = datetime.now()
    # 假設每週任務是固定的，或者需要從某個地方獲取
    # 這裡可以加入更複雜的邏輯來計算本週的待辦事項
    weekly_tasks = f"【本週待辦事項提醒】\n日期：{today.strftime('%Y-%m-%d')} 當週\n\n1. 清理公共區域\n2. 檢查冰箱食物\n3. 採買日用品\n\n祝大家有個愉快的一週！"
    return weekly_tasks

def push_message(to, text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "to": to,
        "messages": [{"type": "text", "text": text}]
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Push message status: {response.status_code}")
    print(f"Push message response: {response.text}")

if __name__ == "__main__":
    message_content = get_weekly_tasks_info()
    if LINE_GROUP_ID == "Cxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx":
        print("錯誤：請在 send_weekly_tasks_reminder.py 中設定正確的 LINE_GROUP_ID。")
    else:
        push_message(LINE_GROUP_ID, message_content)
