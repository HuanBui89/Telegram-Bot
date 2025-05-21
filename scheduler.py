import time
from datetime import datetime, timedelta
from morning_bot import send_morning_message
import pytz

def wait_until(hour: int, minute: int):
    vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(vn_tz)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    delta = (target - now).total_seconds()
    print(f"⏳ Chờ {delta/3600:.2f} giờ để gửi lúc {hour:02d}:{minute:02d}")
    time.sleep(delta)

def run_daily():
    while True:
        wait_until(7, 0)
        try:
            print("⏰ Gửi tin nhắn sáng...")
            send_morning_message()
        except Exception as e:
            print("❌ Lỗi khi gửi:", e)
        # Sau khi gửi xong, chờ 61 phút để chắc chắn không gửi lại nếu Railway restart đúng lúc
        time.sleep(60 * 61)

if __name__ == "__main__":
    run_daily()
