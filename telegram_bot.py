import openai
from telegram import Bot
from datetime import datetime
import pytz
import os

# Lấy từ biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Cấu hình bot và OpenAI
bot = Bot(token=TELEGRAM_TOKEN)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Lấy nội dung văn bản từ GPT
def get_text(prompt):
    print("💬 GPT Prompt:", prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.95,
    )
    return response.choices[0].message.content.strip()

# Tạo ảnh minh họa bằng DALL·E
def create_image(prompt):
    print("🖼️ DALL·E Prompt:", prompt)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        quality="standard"
    )
    return response.data[0].url

# Nội dung động lực theo ngày
weekday_boost = {
    "Monday": "📅 Đầu tuần rồi, bung lụa mở bát thiệt mạnh nha mấy chế! 💪",
    "Tuesday": "📅 Thứ ba không drama – chỉ có đơn đổ ào ào thôi nè! 📈",
    "Wednesday": "📅 Giữa tuần giữ phong độ, đơn về là có động lực liền! 😎",
    "Thursday": "📅 Thứ năm tăng tốc, chạy KPI mượt như nước mắm Nam Ngư! 🚀",
    "Friday": "📅 Cuối tuần nhưng không xả hơi – chốt đơn xong rồi hãy chơi! 🕺",
    "Saturday": "📅 Thứ bảy máu chiến – ai chốt được hôm nay là đỉnh của chóp! 🔥",
    "Sunday": "📅 Chủ nhật chill nhẹ, nhưng ai chốt đơn thì vẫn là người chiến thắng! 🏆",
}

# Gửi lời chúc buổi sáng
def send_morning_message():
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(vietnam_tz)
    today = now.strftime("%A")
    print("📅 Hôm nay là:", today)

    try:
        # Tạo châm ngôn mỗi ngày bằng GPT (Anh + phụ đề Việt)
        quote_en = get_text("Viết một câu châm ngôn truyền động lực ngắn bằng tiếng Anh cho người trẻ đi làm.")
        quote_vi = get_text(f"Dịch nghĩa câu sau sang tiếng Việt theo văn phong Gen Z, tích cực, truyền cảm hứng:\n{quote_en}")
        quote = f"{quote_en}\n_({quote_vi})_"

        # Tạo ảnh minh họa tích cực
        image_prompt = get_text("Mô tả một hình ảnh minh họa tạo động lực buổi sáng cho Gen Z – phong cách trẻ trung, năng động, tươi sáng, tranh 4D, phù hợp với dân văn phòng sales.")
        image_url = create_image(image_prompt)

        # Soạn nội dung
        greeting = "Chào buổi sáng team sales! ☀️"
        daily_line = weekday_boost.get(today, "")
        caption = f"{greeting}\n{daily_line}\n\n💡 **Châm ngôn hôm nay:**\n{quote}"

        # Gửi ảnh + caption
        bot.send_photo(chat_id=GROUP_CHAT_ID, photo=image_url, caption=caption, parse_mode='Markdown')

        print("✅ Đã gửi lời chúc kèm ảnh thành công!")

    except Exception as e:
        print("❌ Gửi thất bại:", str(e))
        print("🪵 Chi tiết lỗi:", repr(e))

# Gọi khi chạy
if __name__ == "__main__":
    send_morning_message()
