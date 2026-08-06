from telethon import TelegramClient

API_ID = 30494584
API_HASH = "239fcf1a4c472e26e3b550d1d4551dab"

client = TelegramClient("user.session", API_ID, API_HASH)
client.start()
print("✅ Session created successfully!")
