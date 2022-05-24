import asyncio
from FlameMusic import app, OWNER
from pyrogram import filters, Client
from pyrogram.types import Message
from FlameMusic.FlameMusicUtilities.database.chats import (get_served_chats, is_served_chat, add_served_chat, get_served_chats)
from ..FlameMusicUtilities.helpers.filters import command


@app.on_message(filters.command("broadcast_pin") & filters.user(OWNER))
async def broadcast_message_pin(_, message):
    if not message.reply_to_message:
        pass
    else :
        x = message.reply_to_message.message_id   
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=False)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"✅ **Mᴇssᴀɢᴇs ʙʀᴏᴀᴅᴄᴀsᴛ ᴏɴ {sent} ᴄʜᴀᴛ\n\n📌 ᴡɪᴛʜ {pin} ᴘɪɴ.**")  
        return
    if len(message.command) < 2:
        await message.reply_text("**Cᴏɴsᴜᴍᴘᴛɪᴏɴ**:\n/broadcast (message)")
        return  
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=False)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"✅ **ʙʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛᴛᴇᴅ ᴏɴ {sent} ᴄʜᴀᴛ\n📌 ᴡɪᴛʜ {pin} pin.**")


@app.on_message(filters.command("broadcast") & filters.user(OWNER))
async def broadcast_message_nopin(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"✅ **Mᴇssᴀɢᴇs ʙʀᴏᴀᴅᴄᴀsᴛ ɪn {sent} ᴄʜᴀᴛ")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**usage**:\n/broadcast (message)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"✅ **Mᴇssᴀɢᴇs ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ {sent} chat")
