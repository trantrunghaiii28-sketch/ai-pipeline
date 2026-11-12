import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# ===== 1. Đọc API key từ file .env =====
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("LỖI: Không tìm thấy GEMINI_API_KEY.")
    print("-> Kiểm tra file .env nằm cùng thư mục và có dòng GEMINI_API_KEY=...")
    raise SystemExit(1)

print(f"[OK] Đã đọc key (dài {len(api_key)} ký tự)")
client = genai.Client(api_key=api_key)


def giai_thich_loi(e):
    """In lời giải thích dễ hiểu cho từng loại lỗi."""
    print(f"\n[LỖI {e.code}] {e.message}\n")
    if e.code == 403:
        print("-> Key bị từ chối. Thường do project chưa có quyền dùng gói miễn phí.")
        print("   Thử tạo key mới trong project mới, hoặc bật billing tại")
        print("   https://aistudio.google.com/billing")
        print("-> Tên model không còn tồn tại. Hãy chạy lại, code sẽ tự tìm model mới.")
    elif e.code == 429:
        print("-> Gọi quá nhiều lần hoặc hết hạn mức. Chờ 1 phút rồi thử lại.")
    elif e.code in (400, 401):
        print("-> Key sai hoặc bị thừa/thiếu ký tự. Dán lại key vào file .env.")
    else:
        print("-> Lỗi khác. Chụp lại màn hình Terminal để được hỗ trợ.")


# ===== 2. Tìm model đang dùng được =====
try:
    tat_ca = [m.name.replace("models/", "") for m in client.models.list()]
except errors.APIError as e:
    giai_thich_loi(e)
    raise SystemExit(1)

# Chỉ lấy các model chat dạng "flash" (nhanh, rẻ), bỏ model ảnh/giọng nói
bo_qua = ("image", "tts", "audio", "live", "embedding", "vision", "robotics")
ung_vien = [
    n for n in tat_ca
    if n.startswith("gemini") and "flash" in n and not any(k in n for k in bo_qua)
]

if not ung_vien:
    print("Không tìm thấy model flash nào. Danh sách model của bạn:")
    for n in tat_ca:
        print(" -", n)
    raise SystemExit(1)

model = sorted(ung_vien)[-1]  # lấy tên "lớn nhất" thường là bản mới nhất
print(f"[OK] Sẽ dùng model: {model}")

# ===== 3. Gửi câu hỏi thử =====
try:
    response = client.models.generate_content(
        model=model,
        contents="Xin chào! Hãy giới thiệu ngắn gọn về bạn trong 2 câu.",
    )
    print("\n===== GEMINI TRẢ LỜI =====")
    print(response.text)
except errors.APIError as e:
    giai_thich_loi(e)