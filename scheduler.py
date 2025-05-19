import time
from datetime import datetime
from morning_bot import send_morning_message
import pytz

def wait_until(hour: int, minute: int):
    while True:
        now = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))
        if now.hour == hour and now.minute == minute:
            return
        time.sleep(30)

def run_daily():
    while True:
        wait_until(7, 0)  # chạy lúc 07:00 ICT
        try:
            print("⏰ Gửi tin nhắn sáng...")
            send_morning_message()
        except Exception as e:
            print("❌ Lỗi khi gửi:", e)
        time.sleep(60)  # chờ tránh lặp lại

if __name__ == "__main__":
    run_daily()
