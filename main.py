import argparse
import os
import asyncio
from datetime import datetime
import pytz
from openai import OpenAI
from telegram import Bot
from PIL import Image
import requests
import io
import traceback

# === Cấu hình ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Kiểm tra biến môi trường
if not all([TELEGRAM_TOKEN, OPENAI_API_KEY, GROUP_CHAT_ID]):
    raise ValueError("⚠️ Thiếu biến môi trường: TELEGRAM_TOKEN, OPENAI_API_KEY hoặc GROUP_CHAT_ID")

# Khởi tạo client
bot = Bot(token=TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# === Cảnh nền thay đổi theo ngày ===
daily_scenes = {
    "Monday": "sunrise over a calm lake with morning mist",
    "Tuesday": "golden rice fields in early sunlight",
    "Wednesday": "sunrise over peaceful ocean waves",
    "Thursday": "lush green hills and valley at dawn",
    "Friday": "mountains with glowing fog and flowers",
    "Saturday": "sunlight on a tropical beach with palm trees",
    "Sunday": "river flowing through peaceful forest in sunrise",
}

# === Lời chúc theo ngày ===
weekday_boost = {
    "Monday": "📅 Đầu tuần rồi, bung lụa mở bát thiệt mạnh nha mấy chế! 💪",
    "Tuesday": "📅 Thứ ba không drama – chỉ có đơn đổ ào ào thôi nè! 📈",
    "Wednesday": "📅 Giữa tuần giữ phong độ, đơn về là có động lực liền! 😎",
    "Thursday": "📅 Thứ năm tăng tốc, chạy KPI mượt như nước mắm Nam Ngư! 🚀",
    "Friday": "📅 Cuối tuần nhưng không xả hơi – chốt đơn xong rồi hãy chơi! 🕺",
    "Saturday": "📅 Thứ bảy máu chiến – ai chốt được hôm nay là đỉnh của chóp! 🔥",
    "Sunday": "📅 Chủ nhật chill nhẹ, nhưng ai chốt đơn thì vẫn là người chiến thắng! 🏆",
}

# === Hàm lấy text từ ChatGPT ===
def get_text(prompt: str, max_tokens=150) -> str:
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # dùng model mới nhất, rẻ hơn, nhanh hơn
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Lỗi khi gọi OpenAI Chat:", e)
        return "Không lấy được châm ngôn hôm nay 😢"

# === Hàm tạo ảnh ===
def create_image(prompt: str) -> str:
    try:
        print("🖼️ Tạo ảnh với prompt:", prompt)
        response = client.images.generate(
            model="gpt-4o-mini",  # hoặc "dall-e-3" nếu tài khoản hỗ trợ
            prompt=prompt,
            size="1024x1024",
            n=1,
        )
        image_url = response.data[0].url
        image_bytes = requests.get(image_url).content
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        os.makedirs("/tmp", exist_ok=True)
        image_path = "/tmp/morning_motivation.png"
        image.save(image_path)
        return image_path
    except Exception as e:
        print("❌ Lỗi khi tạo ảnh:", e)
        traceback.print_exc()
        return None

# === Hàm gửi tin buổi sáng ===
async def send_morning_message():
    try:
        vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        now = datetime.now(vietnam_tz)
        today = now.strftime("%A")
        current_time = now.strftime("%H:%M:%S")

        print(f"🕒 [DEBUG] Giờ hiện tại (ICT): {current_time}")
        print(f"📅 Hôm nay là: {today}")

        # 1. Lấy quote
        quote_en = get_text("Give me one short inspirational quote by a famous person, include the name.")
        quote_vi = get_text(f"Dịch sang tiếng Việt, truyền cảm hứng và dễ hiểu:\n{quote_en}")
        quote = f"“{quote_en}”\n_({quote_vi})_"

        # 2. Tạo ảnh
        scene_prompt = f"A beautiful {daily_scenes.get(today, 'sunrise over mountains')}, ultra-realistic, no text"
        image_path = create_image(scene_prompt)

        # 3. Soạn caption
        greeting = "Chào buổi sáng team sales! ☀️"
        daily_line = weekday_boost.get(today, "")
        caption = f"{greeting}\n{daily_line}\n\n💡 **Châm ngôn hôm nay:**\n{quote}"

        # 4. Gửi Telegram
        if image_path and os.path.exists(image_path):
            print("📤 Đang gửi ảnh lên Telegram...")
            with open(image_path, "rb") as img:
                await bot.send_photo(
                    chat_id=GROUP_CHAT_ID,
                    photo=img,
                    caption=caption,
                    parse_mode="Markdown",
                    read_timeout=30,
                    connect_timeout=15
                )
            print("✅ Đã gửi thành công lúc:", datetime.now(vietnam_tz).strftime("%H:%M:%S"))
        else:
            print("⚠️ Không tạo được ảnh, gửi tin nhắn text thay thế.")
            await bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=caption,
                parse_mode="Markdown"
            )

    except Exception as e:
        print("❌ Lỗi nghiêm trọng:", str(e))
        traceback.print_exc()

# === Entry point ===
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true', help='Gửi tin ngay lập tức')
    args = parser.parse_args()

    if args.once:
        asyncio.run(send_morning_message())

if __name__ == "__main__":
    main()
