import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("PERPLEXITY_API_KEY")
if not key:
    raise SystemExit("LỖI: Chưa có PERPLEXITY_API_KEY trong file .env")

r = requests.post(
    "https://api.perplexity.ai/chat/completions",
    headers={"Authorization": f"Bearer {key}"},
    json={"model": "sonar",
          "messages": [{"role": "user", "content": "Tin công nghệ AI nổi bật tuần này? Trả lời ngắn gọn."}]},
    timeout=60,
)

if r.ok:
    data = r.json()
    print("===== PERPLEXITY TRẢ LỜI =====")
    print(data["choices"][0]["message"]["content"])
    for i, link in enumerate(data.get("citations", []), 1):
        print(f"nguồn [{i}] {link}")
else:
    print(f"[LỖI {r.status_code}]", r.text[:500])
    if r.status_code in (401, 403):
        print("-> Key sai hoặc chưa nạp credit.")