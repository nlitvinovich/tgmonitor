import asyncio
from telethon import TelegramClient
import pandas as pd

API_ID = 30494584
API_HASH = "239fcf1a4c472e26e3b550d1d4551dab"
SESSION_FILE = "user.session"

CHANNEL_USERNAME = 1466753077
OUTPUT_FILE = "channel_messages.xlsx"


async def main():
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.connect()

    # Проверяем авторизацию
    if not await client.is_user_authorized():
        print("❌ Session not authorized — recreate user.session")
        return

    # Получаем канал
    channel = await client.get_entity(CHANNEL_USERNAME)

    messages = []
    async for message in client.iter_messages(channel, limit=1000):
        messages.append({
            "id": message.id,
            "date": message.date,
            "text": message.text,
            "views": message.views,
            "forwards": message.forwards,
            "replies": message.replies.replies if message.replies else 0
        })

    # Сохраняем в Excel
    df = pd.DataFrame(messages)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"✅ Exported {len(messages)} messages to {OUTPUT_FILE}")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
