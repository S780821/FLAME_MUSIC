import os

from FlameMusic import OWNER, app
from FlameMusic.FlameMusicUtilities.database.sudo import add_sudo, get_sudoers, remove_sudo
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command("addsudo") & filters.user(OWNER))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ ᴍᴇssᴀɢᴇs ᴏʀ ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀɴᴀᴍᴇ_ɪᴅ.."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        message.from_user
        sudoers = await get_sudoers()
        if user.id in sudoers:
            return await message.reply_text("ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ.")
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(
                f"ᴀᴅᴅᴇᴅ **{user.mention}** ᴀs ᴀ sᴜᴅᴏ ᴜsᴇʀ"
            )
            return os.execvp("python3", ["python3", "-m", "FlameMusic"])
        await edit_or_reply(message, text="ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ, ᴄʜᴇᴄᴋ ᴛʜᴇ ʟᴏɢ.")
        return
    message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id in sudoers:
        return await message.reply_text("ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ.")
    added = await add_sudo(user_id)
    if added:
        await message.reply_text(f"Added **{mention}** ᴀs ᴀ sᴜᴅᴏ ᴜsᴇʀ")
        return os.execvp("python3", ["python3", "-m", "FlameMusic"])
    await edit_or_reply(message, text="ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ, ᴄʜᴇᴄᴋ ᴛʜᴇ ʟᴏɢ.")
    return


@app.on_message(filters.command("delsudo") & filters.user(OWNER))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ ᴍᴇssᴀɢᴇs ᴏʀ ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        message.from_user
        if user.id not in await get_sudoers():
            return await message.reply_text(f"Not a part of FlameMusic's Sudo.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(f"ᴅᴇʟᴇᴛᴇ **{user.mention}** ғʀᴏᴍ sᴜᴅᴏ.")
            return os.execvp("python3", ["python3", "-m", "FlameMusic"])
        await message.reply_text(f"sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.")
        return
    message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in await get_sudoers():
        return await message.reply_text(f"ɴᴏᴛ ᴘᴀʀᴛ ᴏғ sᴜᴅᴏ ᴍᴜsɪᴄ.")
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(f"ᴅᴇʟᴇᴛᴇ **{mention}** from sudo.")
        return os.execvp("python3", ["python3", "-m", "FlameMusic"])
    await message.reply_text(f"Something wrong happened.")


@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "**sᴜᴅᴏ ᴜsᴇʀ ʟɪsᴛ**\n\n"
    for count, user_id in enumerate(sudoers, 1):
        try:
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
        except Exception:
            continue
        text += f"• {user}\n"
    if not text:
        await message.reply_text("ɴᴏ sᴜᴅᴏ ᴜsᴇʀ")
    else:
        await message.reply_text(text)
