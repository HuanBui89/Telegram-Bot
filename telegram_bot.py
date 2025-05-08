import openai
from telegram import Bot
from datetime import datetime
import pytz
import os

# Lấy từ biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Cấu hình OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)

# Lấy text từ GPT
def get_text(prompt):
    print("💬 GPT Prompt:", prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.9,
    )
    return response.choices[0].message.content.strip()

# Tạo ảnh minh họa
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

# Gửi tin nhắn sáng
def send_morning_message():
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    start_time = datetime.now(vietnam_tz)
    print("🚀 Bắt đầu lúc:", start_time.strftime("%H:%M:%S"))

    try:
        greeting = get_text("Viết lời chúc buổi sáng theo phong cách vui nhộn, trẻ trung, dùng ngôn ngữ Gen Z, dành cho team sales sinh từ 1997–2003. Lời chúc phải tràn đầy năng lượng và tạo cảm hứng làm việc.")
        quote = get_text("Viết một câu châm ngôn tạo động lực ngắn gọn nhưng hài hước, văn phong Gen Z, truyền cảm hứng làm việc cho team sales trẻ.")
        image_prompt = get_text("Mô tả một hình ảnh buổi sáng dễ chịu, tươi sáng, phong cách vui nhộn, nhẹ nhàng để tạo ảnh AI minh họa cho lời chúc buổi sáng.")

        image_url = create_image(image_prompt)

        caption = f"🌞 **Chào buổi sáng Team Sales!**\n\n{greeting}\n\n💡 **Châm ngôn hôm nay:**\n_{quote}_"

        bot.send_photo(chat_id=GROUP_CHAT_ID, photo=image_url, caption=caption, parse_mode='Markdown')

        end_time = datetime.now(vietnam_tz)
        print("✅ Đã gửi lúc:", end_time.strftime("%H:%M:%S"))
        print("⏱️ Tổng thời gian thực thi:", str(end_time - start_time))

    except Exception as e:
        print("❌ Lỗi khi gửi:", str(e))

# Gọi khi chạy
if __name__ == "__main__":
    send_morning_message()
