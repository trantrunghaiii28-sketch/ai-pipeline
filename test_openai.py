import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if not key:
    raise SystemExit("LỖI: Chưa có OPENAI_API_KEY trong file .env")

head = {"Authorization": f"Bearer {key}"}

# Tự tìm model mini đang có (hoặc đặt OPENAI_MODEL=... trong .env)
model = os.getenv("OPENAI_MODEL")
if not model:
    r = requests.get("https://api.openai.com/v1/models", headers=head, timeout=60)
    if not r.ok:
        raise SystemExit(f"[LỖI {r.status_code}] {r.text[:500]}")
    bo_qua = ("audio", "realtime", "transcribe", "tts", "image",
              "search", "instruct", "embedding", "moderation", "codex")
    ds = [m["id"] for m in r.json()["data"]
          if m["id"].startswith("gpt") and "mini" in m["id"]
          and not any(k in m["id"] for k in bo_qua)]
    if not ds:
        raise SystemExit("Không tự tìm được model. Thêm OPENAI_MODEL=ten_model vào .env")
    model = sorted(ds)[-1]
print("Dùng model:", model)

r = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers=head,
    json={"model": model,
          "messages": [{"role": "user", "content": "Xin chào! Giới thiệu ngắn gọn về bạn trong 2 câu."}]},
    timeout=60,
)

if r.ok:
    print("===== CHATGPT TRẢ LỜI =====")
    print(r.json()["choices"][0]["message"]["content"])
else:
    print(f"[LỖI {r.status_code}]", r.text[:500])
    if r.status_code == 401:
        print("-> Key sai.")
    elif r.status_code == 429:
        print("-> Thường do chưa nạp tiền hoặc hết hạn mức.")