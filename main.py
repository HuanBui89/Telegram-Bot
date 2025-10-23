import os
import traceback
import requests
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ==============================
# 🔧 CẤU HÌNH
# ==============================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "sk-xxx"  # Thay bằng key thật nếu test local
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "xxxxx"  # Token bot Telegram

client = OpenAI(api_key=OPENAI_API_KEY)

# ==============================
# 🖼️ HÀM TẠO ẢNH BẰNG DALL·E 3
# ==============================
def create_image(prompt: str) -> str:
    try:
        print("🖌️ Đang tạo ảnh bằng DALL·E 3...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1,
        )

        image_url = response.data[0].url
        print("🖼️ Ảnh tạo xong:", image_url)

        image_bytes = requests.get(image_url).content
        os.makedirs("/tmp", exist_ok=True)
        image_path = "/tmp/dalle3_output.png"

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        print(f"✅ Ảnh đã lưu tại {image_path} ({len(image_bytes)/1024:.1f} KB)")
        return image_path

    except Exception as e:
        print("❌ Lỗi khi tạo ảnh DALL·E 3:", e)
        traceback.print_exc()
        return None

# ==============================
# 💬 HÀM TRẢ LỜI CHAT
# ==============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"💬 Nhận tin nhắn: {user_message}")

    # Tạo prompt cho DALL·E 3
    prompt = f"Tạo ảnh thật, phong cảnh tự nhiên, ánh sáng đẹp, phong cách nhiếp ảnh: {user_message}"

    await update.message.reply_text("🖌️ Đang tạo ảnh bằng DALL·E 3... (chờ vài giây)")

    image_path = create_image(prompt)

    if image_path:
        print("📤 Đang gửi ảnh lên Telegram...")
        await update.message.reply_photo(photo=open(image_path, "rb"))
        print("✅ Đã gửi ảnh thành công.")
    else:
        await update.message.reply_text("❌ Không tạo được ảnh. Thử mô tả khác nhé!")

# ==============================
# 🚀 KHỞI CHẠY BOT
# ==============================
def main():
    print("🚀 Khởi động bot Telegram (DALL·E 3)...")
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot đã sẵn sàng! Gửi tin nhắn để tạo ảnh.")
    application.run_polling()

# ==============================
# 🏁 MAIN
# ==============================
if __name__ == "__main__":
    main()
