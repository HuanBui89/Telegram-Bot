import openai
from telegram import Bot
import schedule
import time
import os

# Lấy các biến môi trường từ GitHub Actions Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHATGPT_API_KEY = os.getenv("OPENAI_API_KEY")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Kiểm tra nếu thiếu biến
if not TELEGRAM_TOKEN or not CHATGPT_API_KEY or not GROUP_CHAT_ID:
    raise ValueError("❌ Thiếu biến môi trường! Vui lòng kiểm tra TELEGRAM_TOKEN, OPENAI_API_KEY, GROUP_CHAT_ID.")

# Khởi tạo bot và API
openai.api_key = CHATGPT_API_KEY
bot = Bot(token=TELEGRAM_TOKEN)

def get_message(prompt):
    print(f"💬 Gửi prompt tới ChatGPT: {prompt}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Bạn là một trợ lý gửi lời chúc mỗi ngày."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.8,
    )
    return response['choices'][0]['message']['content'].strip()

def send_morning_message():
    print("🔧 Bắt đầu gửi tin nhắn...")

    greeting_prompt = "Viết một câu chúc buổi sáng tốt lành, vui vẻ và tràn đầy năng lượng cho team sales."
    quote_prompt = "Viết một câu châm ngôn hoặc câu nói truyền động lực ngắn gọn cho team sales."

    try:
        greeting = get_message(greeting_prompt)
        print("✅ Greeting:", greeting)

        quote = get_message(quote_prompt)
        print("✅ Quote:", quote)

        full_message = f"🌞 **Chào buổi sáng Team Sales!**\n\n{greeting}\n\n💡 **Châm ngôn hôm nay:**\n_{quote}_"

        bot.send_message(chat_id=GROUP_CHAT_ID, text=full_message, parse_mode='Markdown')
        print("✅ Tin nhắn đã gửi thành công!")

    except Exception as e:
        print("❌ Lỗi khi gửi tin nhắn:", str(e))

# Lên lịch chạy mỗi ngày lúc 8h sáng (nếu chạy cục bộ)
schedule.every().day.at("08:00").do(send_morning_message)

# Nếu chạy trên GitHub Actions, gọi trực tiếp một lần
if __name__ == "__main__":
    send_morning_message()
