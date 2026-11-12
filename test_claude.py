import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("ANTHROPIC_API_KEY")
if not key:
    raise SystemExit("LỖI: Chưa có ANTHROPIC_API_KEY trong file .env")

r = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    },
    json={
        "model": "claude-haiku-5-5",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": "Xin chào! Giới thiệu ngắn gọn về bạn trong 2 câu."}],
    },
    timeout=60,
)

if r.ok:
    print("===== CLAUDE TRẢ LỜI =====")
    print(r.json()["content"][0]["text"])
else:
    print(f"[LỖI {r.status_code}]", r.text[:500])
    if r.status_code == 401:
        print("-> Key sai.")
    elif r.status_code == 400:
        print("-> Thường do chưa nạp tiền (credit) trong Plans & Billing.")
    elif r.status_code == 404:
        print("-> Tên model sai.")