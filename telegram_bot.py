import argparse
import os
from datetime import datetime
import pytz
import openai
from telegram import Bot
from PIL import Image, ImageDraw, ImageFont
import requests
import io
import textwrap

# Lấy từ biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Cấu hình bot và OpenAI
bot = Bot(token=TELEGRAM_TOKEN)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Cảnh nền theo ngày
daily_scenes = {
    "Monday": "sunrise over a calm lake with morning mist",
    "Tuesday": "golden rice fields in early sunlight",
    "Wednesday": "sunrise over peaceful ocean waves",
    "Thursday": "lush green hills and valley at dawn",
    "Friday": "mountains with glowing fog and flowers",
    "Saturday": "sunlight on a tropical beach with palm trees",
    "Sunday": "river flowing through peaceful forest in sunrise",
}

# Lời chúc động lực
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

def create_image(prompt: str) -> Image.Image:
    """Gọi DALL·E, tải ảnh về và trả về đối tượng PIL"""
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
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")

def draw_quote_on_image(image: Image.Image, en: str, vi: str) -> Image.Image:
    """Chèn châm ngôn + dịch nghĩa lên ảnh"""
    draw = ImageDraw.Draw(image)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(font_path, 28)

    margin = 40
    max_width = image.width - 2 * margin
    text = f"{en}\n({vi})"
    wrapped = textwrap.fill(text, width=50)

    bbox = draw.textbbox((0, 0), wrapped, font=font)
    x = margin
    y = image.height - (bbox[3] - bbox[1]) - 60

    # Nền mờ cho chữ
    draw.rectangle(
        [x - 10, y - 10, x + max_width, y + (bbox[3] - bbox[1]) + 20],
        fill=(0, 0, 0, 180)
    )
    # Chữ trắng
    draw.text((x, y), wrapped, font=font, fill="white")
    return image

def send_morning_message():
    """Soạn và gửi tin chào buổi sáng có ảnh và châm ngôn in sẵn"""
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(vietnam_tz)
    today = now.strftime("%A")
    print("📅 Hôm nay là:", today)

    try:
        # 1. Châm ngôn và dịch
        quote_en = get_text("Trích dẫn một câu châm ngôn nổi tiếng từ danh nhân và ghi rõ người nói.")
        quote_vi = get_text(f"Dịch sang tiếng Việt dễ hiểu, truyền cảm hứng:\n{quote_en}")

        # 2. Tạo ảnh theo ngày
        scene_prompt = f"A beautiful {daily_scenes.get(today, 'sunrise over mountains')}, ultra-realistic, no text"
        base_image = create_image(scene_prompt)

        # 3. Vẽ chữ vào ảnh
        final_image = draw_quote_on_image(base_image, quote_en, quote_vi)

        # 4. Lưu ảnh tạm
        image_path = "/tmp/morning_motivation.png"
        final_image.save(image_path)

        # 5. Caption
        greeting = "Chào buổi sáng team sales! ☀️"
        daily_line = weekday_boost.get(today, "")
        caption = f"{greeting}\n{daily_line}"

        # 6. Gửi Telegram
        with open(image_path, "rb") as img:
            bot.send_photo(
                chat_id=GROUP_CHAT_ID,
                photo=img,
                caption=caption
            )
        print("✅ Đã gửi lời chúc kèm ảnh thành công!")

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
