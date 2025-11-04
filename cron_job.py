# cron_job.py
import asyncio
from main import send_daily_report  # giả sử bạn có hàm này

asyncio.run(send_daily_report())
print("✅ Cron job executed successfully")
