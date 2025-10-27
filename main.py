import os
import asyncio
import requests
from datetime import datetime
import pytz
from openai import OpenAI
from telegram import Bot

# ============ CẤU HÌNH ============
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "xxx"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "sk-xxx"
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID") or "xxx"

bot = Bot(token=TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

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

# ============ HÀM OPENAI ============
def get_text(prompt: str, max_tokens=150) -> str:
    """Lấy nội dung từ ChatGPT"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

def create_image(prompt: str) -> str:
    """Tạo ảnh từ DALL·E 3 và lưu vào local"""
    print("🖌️ Tạo ảnh với prompt:", prompt)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    image_bytes = requests.get(image_url).content

    os.makedirs("/tmp", exist_ok=True)
    image_path = "/tmp/morning_motivation.png"
    with open(image_path, "wb") as f:
        f.write(image_bytes)

    print("✅ Ảnh đã lưu tại:", image_path)
    return image_path

# ============ HÀM GỬI TELEGRAM ============
async def send_morning_message():
    """Gửi tin buổi sáng kèm ảnh động lực"""
    try:
        # 1. Xác định thời gian
        vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        now = datetime.now(vietnam_tz)
        current_time = now.strftime("%H:%M:%S")
        today = now.strftime("%A")
        print(f"🕒 [DEBUG] Thời gian chạy thực tế (ICT): {current_time}")
        print(f"📅 Hôm nay là: {today}")

        # 2. Lấy quote
        quote_en = get_text("Trích dẫn một câu châm ngôn nổi tiếng từ danh nhân và ghi rõ người nói.")
        quote_vi = get_text(f"Dịch sang tiếng Việt dễ hiểu, truyền cảm hứng:\n{quote_en}")
        quote = f"“{quote_en}”\n_{quote_vi}_"

        # 3. Tạo ảnh
        scene_prompt = f"A beautiful {daily_scenes.get(today, 'sunrise over mountains')}, ultra-realistic, no text"
        image_path = create_image(scene_prompt)

        # 4. Soạn nội dung
        greeting = "Chào buổi sáng team sales! ☀️"
        daily_line = weekday_boost.get(today, "")
        caption = f"{greeting}\n{daily_line}\n\n💡 *Châm ngôn hôm nay:*\n{quote}"

        # 5. Gửi Telegram (phải await)
        async with bot:
            with open(image_path, "rb") as img:
                await bot.send_photo(
                    chat_id=GROUP_CHAT_ID,
                    photo=img,
                    caption=caption,
                    parse_mode="Markdown",
                )
        print("✅ Đã gửi thành công lúc:", datetime.now(vietnam_tz).strftime("%H:%M:%S"))

    except Exception as e:
        print("❌ Lỗi nghiêm trọng:", str(e))

# ============ MAIN ============

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok", "message": "Telegram bot is alive"}

@app.get("/run")
async def run_now():
    await send_morning_message()
    return {"status": "done"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
