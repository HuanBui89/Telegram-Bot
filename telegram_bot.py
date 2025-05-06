import openai
from telegram import Bot
import os

# Đọc từ biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Kiểm tra biến
if not TELEGRAM_TOKEN or not OPENAI_API_KEY or not GROUP_CHAT_ID:
    raise ValueError("Thiếu biến môi trường")

# Cấu hình OpenAI mới
client = openai.OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)

def get_message(prompt):
    print("💬 Gửi prompt tới ChatGPT:", prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Bạn là một trợ lý gửi lời chúc mỗi ngày."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()

def send_morning_message():
    print("🔧 Bắt đầu gửi tin nhắn...")

    try:
        greeting_prompt = "Viết một câu chúc buổi sáng tốt lành, vui vẻ và tràn đầy năng lượng cho team sales."
        quote_prompt = "Viết một câu châm ngôn hoặc câu nói truyền động lực ngắn gọn cho team sales."

        greeting = get_message(greeting_prompt)
        print("✅ Greeting:", greeting)

        quote = get_message(quote_prompt)
        print("✅ Quote:", quote)

        full_message = f"🌞 **Chào buổi sáng Team Sales!**\n\n{greeting}\n\n💡 **Châm ngôn hôm nay:**\n_{quote}_"

        bot.send_message(chat_id=GROUP_CHAT_ID, text=full_message, parse_mode='Markdown')
        print("✅ Tin nhắn đã gửi thành công!")

    except Exception as e:
        print("❌ Lỗi khi gửi tin nhắn:", str(e))

# Gọi ngay
if __name__ == "__main__":
    send_morning_message()
