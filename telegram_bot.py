import openai
from telegram import Bot
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
        temperature=0.8,
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
    print("🔧 Bắt đầu gửi chúc buổi sáng...")

    try:
        greeting = get_text("Viết một câu chúc buổi sáng tốt lành, tràn đầy năng lượng cho team sales.")
        quote = get_text("Viết một câu châm ngôn truyền động lực ngắn gọn cho team sales.")
        image_prompt = get_text("Viết mô tả hình ảnh minh họa buổi sáng dễ chịu, phong cách nhẹ nhàng tích cực, dùng để tạo ảnh bằng AI.")

        image_url = create_image(image_prompt)

        caption = f"🌞 **Chào buổi sáng Team Sales!**\n\n{greeting}\n\n💡 **Châm ngôn hôm nay:**\n_{quote}_"

        bot.send_photo(chat_id=GROUP_CHAT_ID, photo=image_url, caption=caption, parse_mode='Markdown')
        print("✅ Đã gửi ảnh và lời chúc!")

    except Exception as e:
        print("❌ Lỗi khi gửi:", str(e))

# Gọi khi chạy
if __name__ == "__main__":
    send_morning_message()
