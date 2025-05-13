def send_morning_message():
    """Soạn và gửi tin chào buổi sáng kèm ảnh và thơ lục bát"""
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(vietnam_tz)
    today = now.strftime("%A")
    print("📅 Hôm nay là:", today)

    try:
        # Lấy bài thơ lục bát tạo động lực
        poem = get_text(
            "Hãy viết một bài thơ lục bát gồm 4 câu, mang tinh thần tích cực, truyền động lực cho dân sales làm việc mỗi sáng. "
            "Văn phong trẻ trung, vui vẻ, dễ hiểu, có vần điệu, tránh dùng từ cổ."
        )

        # Tạo ảnh minh họa buổi sáng
        image_url = create_image(IMAGE_PROMPT)

        # Soạn caption và gửi
        greeting   = "Chào buổi sáng team sales! ☀️"
        daily_line = weekday_boost.get(today, "")
        caption = f"{greeting}\n{daily_line}\n\n📝 **Thơ hôm nay:**\n{poem}"

        bot.send_photo(
            chat_id=GROUP_CHAT_ID,
            photo=image_url,
            caption=caption,
            parse_mode='Markdown'
        )
        print("✅ Đã gửi lời chúc kèm ảnh và thơ thành công!")

    except Exception as e:
        print("❌ Gửi thất bại:", str(e))
        print("🪵 Chi tiết lỗi:", repr(e))
