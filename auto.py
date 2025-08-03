import asyncio
import random
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

apiId = 27074275
apiHash = "89b5cde6d92d1cdc19d2108d63185cac"
sessionName = "autoReactAll"

emojiList = ["❤️", "👍", "👎", "🔥", "🎉", "😆", "😢", "😮", "😡"]

client = TelegramClient(sessionName, apiId, apiHash)

@client.on(events.NewMessage)
async def onMessage(event):
    emoji = random.choice(emojiList)
    try:
        await client(SendReactionRequest(
            peer=event.chat_id,
            msg_id=event.id,
            reaction=[ReactionEmoji(emoticon=emoji)]
        ))
        print(f"✅ Reacted {emoji} to msg {event.id} in chat {event.chat_id}")
    except FloodWaitError as e:
        print(f"⏳ Flood wait: sleeping {e.seconds} seconds")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print(f"❌ Failed to react to msg {event.id} in chat {event.chat_id}: {e}")
    finally:
        delay = random.randint(1, 5)
        print(f"⏱️ Waiting {delay} seconds before next reaction...")
        await asyncio.sleep(delay)

async def main():
    print("🤖 AutoReaction bot started")
    await client.run_until_disconnected()

client.start()
client.loop.run_until_complete(main())
