import openai
from telegram import Bot
import schedule
import time

# Thay đổi các giá trị bên dưới
TELEGRAM_TOKEN = "TOKEN_TELEGRAM_CỦA_BẠN"
CHATGPT_API_KEY = "OPENAI_API_KEY_CỦA_BẠN"
GROUP_CHAT_ID = "ID_GROUP_CỦA_BẠN"

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
