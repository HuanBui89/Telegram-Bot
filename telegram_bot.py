import argparse
import os
from datetime import datetime
import pytz
import openai
from telegram import Bot

# Lấy từ biến môi trường
TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY")
GROUP_CHAT_ID    = os.getenv("GROUP_CHAT_ID")

# Cấu hình bot và OpenAI
bot    = Bot(token=TELEGRAM_TOKEN)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Prompt cố định cho ảnh mỗi buổi sáng
IMAGE_PROMPT = (
    "A fresh, vibrant morning nature scene: "
    "misty green hills and a sun rising softly in the sky, "
    "a rustic wooden table in the foreground with a steaming cup of coffee, "
    "bright wildflowers on the side — conveys calm energy and positivity."
)

# Nội dung động lực theo ngày
weekday_boost = {
    "Monday":    "📅 Đầu tuần rồi, bung lụa mở bát thiệt mạnh nha mấy chế! 💪",
    "Tuesday":   "📅 Thứ ba không drama – chỉ có đơn đổ ào ào thôi nè! 📈",
    "Wednesday": "📅 Giữa tuần giữ phong độ, đơn về là có động lực liền! 😎",
    "Thursday":  "📅 Thứ năm tăng tốc, chạy KPI mượt như nước mắm Nam Ngư! 🚀",
    "Friday":    "📅 Cuối tuần nhưng không xả hơi – chốt đơn xong rồi hãy chơi! 🕺",
    "Saturday":  "📅 Thứ bảy máu chiến – ai chốt được hôm nay là đỉnh của chóp! 🔥",
    "Sunday":    "📅 Chủ nhật chill nhẹ, nhưng ai chốt đơn thì vẫn là người chiến thắng! 🏆",
}

def get_text(prompt: str) -> str:
    """Gọi OpenAI ChatCompletion để lấy text"""
    print("💬 GPT Prompt:", prompt)
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.95,
    )
    return resp.choices[0].message.content.strip()

def create_image(prompt: str) -> str:
    """Gọi DALL·E để tạo ảnh, trả về URL"""
    print("🖼️ DALL·E Prompt:", prompt)
    resp = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        quality="standard"
    )
    return resp.data[0].url

def send_morning_message():
    """Soạn và gửi tin chào buổi sáng kèm ảnh"""
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(vietnam_tz)
    today = now.strftime("%A")
    print("📅 Hôm nay là:", today)

    try:
        # Lấy châm ngôn tiếng Anh + dịch Gen Z sang Việt
        quote_en = get_text("Viết một câu châm ngôn truyền động lực ngắn bằng tiếng Anh cho người trẻ đi làm.")
        quote_vi = get_text(
            f"Dịch nghĩa câu sau sang tiếng Việt theo văn phong Gen Z, tích cực, truyền cảm hứng:\n{quote_en}"
        )
        quote = f"{quote_en}\n_({quote_vi})_"

        # Tạo ảnh minh họa cố định
        image_url = create_image(IMAGE_PROMPT)

        # Soạn caption và gửi
        greeting   = "Chào buổi sáng team sales! ☀️"
        daily_line = weekday_boost.get(today, "")
        caption = f"{greeting}\n{daily_line}\n\n💡 **Châm ngôn hôm nay:**\n{quote}"

        bot.send_photo(
            chat_id=GROUP_CHAT_ID,
            photo=image_url,
            caption=caption,
            parse_mode='Markdown'
        )
        print("✅ Đã gửi lời chúc kèm ảnh thành công!")

    except Exception as e:
        print("❌ Gửi thất bại:", str(e))
        print("🪵 Chi tiết lỗi:", repr(e))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--once',
        action='store_true',
        help='Gửi tin ngay lập tức rồi thoát'
    )
    args = parser.parse_args()

    if args.once:
        send_morning_message()
        return

    # Nếu bạn vẫn muốn giữ scheduling bên trong script (không khuyến nghị):
    # import schedule, time
    # schedule.every().day.at("07:20").do(send_morning_message)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(30)

if __name__ == "__main__":
    main()
