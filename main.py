import os
import time
import requests
import schedule
from dotenv import load_dotenv

# Завантажуємо змінні з .env (працює локально, на Render зчитає з Environment Variables)
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    raise ValueError(
        "Не знайдено TELEGRAM_TOKEN або CHAT_ID у змінних оточення!"
    )

CHAT_ID = int(CHAT_ID)
URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN.strip()}/sendPoll"

POLLS = [
    {
        "question": "❓Хто буде присутнім на тренуванні на 9:00?",
        "options": ["✅Так", "❌Ні"],
    },
    {
        "question": "❓Хто буде присутнім на тренуванні на 10:00?",
        "options": ["✅Так", "❌Ні"],
    },
    {
        "question": "❓Хто буде присутнім на тренуванні на 19:45?",
        "options": ["✅Так", "❌Ні"],
    },
]


def send_all_polls():
    print(
        f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Запуск відправки опитувань..."
    )

    for poll_data in POLLS:
        payload = {
            "chat_id": CHAT_ID,
            "question": poll_data["question"],
            "options": poll_data["options"],
            "is_anonymous": False,
        }

        try:
            response = requests.post(URL, json=payload)
            result = response.json()

            if result.get("ok"):
                print(f"✅ Відправлено: {poll_data['question']}")
            else:
                print(f"❌ Помилка при відправці: {result}")
        except Exception as e:
            print(f"❌ Помилка запиту: {e}")

        time.sleep(1)


# Розклад відправки (Нд, Вт, Чт о 21:00)
schedule.every().sunday.at("21:00").do(send_all_polls)
schedule.every().tuesday.at("21:00").do(send_all_polls)
schedule.every().thursday.at("21:00").do(send_all_polls)

print("🚀 Бот запущений на хостингу та чекає розкладу...")

# Безперервний цикл роботи бота
try:
    while True:
        schedule.run_pending()
        time.sleep(10)
except KeyboardInterrupt:
    print("⏹ Планувальник зупинено.")