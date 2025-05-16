import argparse
import os
from datetime import datetime
import pytz
import openai
from telegram import Bot
from PIL import Image
import requests
import io

# Lấy từ biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Cấu hình bot và OpenAI
bot = Bot(token=TELEGRAM_TOKEN)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Cảnh nền thay đổi theo ngày
daily_scenes = {
    "Monday": "sunrise over a calm lake with morning mist",
    "Tuesday": "golden rice fields in early sunlight",
    "Wednesday": "sunrise over peaceful ocean waves",
    "Thursday": "lush green hills and valley at dawn",
    "Friday": "mountains with glowing fog and flowers",
    "Saturday": "sunlight on a tropical beach with palm trees",
    "Sunday": "river flowing through peaceful forest in sunrise",
}

# Lời chúc theo ngày
weekday_boost = {
    "Monday": "📅 Đầu tuần rồi, bung lụa mở bát thiệt mạnh nha mấy chế! 💪",
    "Tuesday": "📅 Thứ ba không drama – chỉ có đơn đổ ào ào thôi nè! 📈",
    "Wednesday": "📅 Giữa tuần giữ phong độ, đơn về là có động lực liền! 😎",
    "Thursday": "📅 Thứ năm tăng tốc, chạy KPI mượt như nước mắm Nam Ngư! 🚀",
    "Friday": "📅 Cuối tuần nhưng không xả hơi – chốt đơn xong rồi hãy chơi! 🕺",
    "Saturday": "📅 Thứ bảy máu chiến – ai chốt được hôm nay là đỉnh của chóp! 🔥",
    "Sunday": "📅 Chủ nhật chill nhẹ, nhưng ai chốt đơn thì vẫn là người chiến thắng! 🏆",
}

def get_text(prompt: str, max_tokens=150) -> str:
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

def create_image(prompt: str) -> str:
    """Tạo ảnh từ DALL·E và lưu vào local, trả về đường dẫn file"""
    print("🖼️ Tạo ảnh với prompt:", prompt)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    image_bytes = requests.get(image_url).content
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    image_path = "/tmp/morning_motivation_clean.png"
    image.save(image_path)
    return image_path

def send_morning_message():
    """Tạo ảnh, lấy quote, và gửi lên Telegram với ảnh sạch (không chèn chữ)"""
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(vietnam_tz)
    today = now.strftime("%A")
    print("📅 Hôm nay là:", today)

    try:
        # 1. Lấy quote + dịch
        quote_en = get_text("Trích dẫn một câu châm ngôn nổi tiếng từ danh nhân và ghi rõ người nói.")
        quote_vi = get_text(f"Dịch sang tiếng Việt dễ hiểu, truyền cảm hứng:\n{quote_en}")
        quote = f"“{quote_en}”\n_({quote_vi})_"

        # 2. Tạo ảnh nền
        scene_prompt = f"A beautiful {daily_scenes.get(today, 'sunrise over mountains')}, ultra-realistic, no text"
        image_path = create_image(scene_prompt)

        # 3. Soạn caption
        greeting = "Chào buổi sáng team sales! ☀️"
        daily_line = weekday_boost.get(today, "")
        caption = f"{greeting}\n{daily_line}\n\n💡 **Châm ngôn hôm nay:**\n{quote}"

        # 4. Gửi Telegram
        with open(image_path, "rb") as img:
            bot.send_photo(
                chat_id=GROUP_CHAT_ID,
                photo=img,
                caption=caption,
                parse_mode="Markdown"
            )

        print("✅ Đã gửi ảnh và nội dung thành công!")

    except Exception as e:
        print("❌ Gửi thất bại:", str(e))
        print("🪵 Chi tiết lỗi:", repr(e))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true', help='Gửi tin ngay lập tức rồi thoát')
    args = parser.parse_args()

    if args.once:
        send_morning_message()

if __name__ == "__main__":
    main()
