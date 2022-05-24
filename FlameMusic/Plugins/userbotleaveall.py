import asyncio

from FlameMusic import BOT_USERNAME, SUDOERS
from FlameMusic import client as USER
from FlameMusic.FlameMusicUtilities.helpers.filters import command
from pyrogram import Client, filters


@Client.on_message(
    command(["userbotleaveall", f"userbotleaveall@{BOT_USERNAME}"])
    & filters.user(SUDOERS)
    & ~filters.edited
)
async def bye(client, message):
    if message.from_user.id in SUDOERS:
        left = 0
        failed = 0
        lol = await message.reply("ᴀssɪsᴛᴀɴᴛ ʟᴇᴀᴠᴇ ᴀʟʟ ᴄʜᴀᴛs")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left + 1
                await lol.edit(
                    f"""
**🔄 ᴘʀᴏᴄᴇssɪɴɢ**

**✅ ɢᴇᴛ ᴏᴜᴛ {left}**
**❌ ғᴀɪʟ {failed}**
"""
                )
            except:
                failed = failed + 1
                await lol.edit(
                    f"""
**🔄 Processing**

**✅ Get out: {left}**
**❌ Fail {failed}**
"""
                )
            await asyncio.sleep(10)
        await lol.delete()
        await client.send_message(
            message.chat.id,
            f"""
**💡 ᴀssɪsᴛᴀɴᴛ ɪs ᴏᴜᴛ**

**✅ Get out {left}**
**❌ Fail {failed}**
""",
        )
