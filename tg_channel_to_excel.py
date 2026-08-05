import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
import pandas as pd

# Загружаем .env
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CHANNEL_LINK = os.getenv("CHANNEL_LINK")
EXCEL_FILE = os.getenv("EXCEL_FILE")

# Инициализация клиента
client = TelegramClient("session_user", API_ID, API_HASH)


# -----------------------------
# Сохранение в Excel
# -----------------------------
def save_to_excel(messages_data):
    if not messages_data:
        print("[Excel] Нет данных для сохранения")
        return

    df = pd.DataFrame(messages_data)

    # Убираем таймзоны — иначе Excel падает
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

    if "edit_date" in df.columns:
        df["edit_date"] = pd.to_datetime(df["edit_date"]).dt.tz_localize(None)

    df.to_excel(EXCEL_FILE, index=False)
    print(f"[Excel] Сохранено {len(df)} сообщений в {EXCEL_FILE}")


# -----------------------------
# Основная функция
# -----------------------------
async def main():
    await client.start(PHONE_NUMBER)
    print("[TG] Клиент запущен как пользователь")

    channel = await client.get_entity(CHANNEL_LINK)
    print(f"[TG] Выгружаем канал: {channel.title}")

    messages_data = []

    async for msg in client.iter_messages(channel, limit=None):
        messages_data.append({
            "id": msg.id,
            "date": msg.date,
            "text": msg.text,
            "edited": msg.edit_date is not None,
            "edit_date": msg.edit_date,
            "link": f"https://t.me/{channel.username}/{msg.id}" if channel.username else ""
        })

    print(f"[TG] История загружена: {len(messages_data)} сообщений")

    save_to_excel(messages_data)

    print("[TG] Готово. Завершаем работу.")
    await client.disconnect()


# -----------------------------
# Запуск
# -----------------------------
if __name__ == "__main__":
    asyncio.run(main())
