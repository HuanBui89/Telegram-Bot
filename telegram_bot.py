import openai
from telegram import Bot
import schedule
import time
import os

# Đọc giá trị token và keys từ biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHATGPT_API_KEY = os.getenv("OPENAI_API_KEY")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Kiểm tra nếu thiếu bất kỳ giá trị nào
if not TELEGRAM_TOKEN or not CHATGPT_API_KEY or not GROUP_CHAT_ID:
    raise ValueError("Thiếu thông tin cấu hình. Vui lòng kiểm tra các biến môi trường.")

openai.api_key = CHATGPT_API_KEY
bot = Bot(token=TELEGRAM_TOKEN)

def get_message(prompt):
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
    greeting_prompt = "Viết một câu chúc buổi sáng tốt lành, vui vẻ và tràn đầy năng lượng cho team sales."
    quote_prompt = "Viết một câu châm ngôn hoặc câu nói truyền động lực ngắn gọn cho team sales."

    greeting = get_message(greeting_prompt)
    quote = get_message(quote_prompt)

    full_message = f"🌞 **Chào buổi sáng Team Sales!**\n\n{greeting}\n\n💡 **Châm ngôn hôm nay:**\n_{quote}_"

    bot.send_message(chat_id=GROUP_CHAT_ID, text=full_message, parse_mode='Markdown')
    print("Đã gửi thông điệp buổi sáng!")

# Lên lịch chạy mỗi ngày lúc 8 giờ sáng
schedule.every().day.at("08:00").do(send_morning_message)

print("Bot đang chạy, chờ gửi tin nhắn mỗi ngày lúc 08:00...")
while True:
    schedule.run_pending()
    time.sleep(30)
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
        print("✅ Đã gửi thông điệp buổi sáng!")
    except Exception as e:
        print("❌ Lỗi khi gửi tin nhắn:", str(e))
