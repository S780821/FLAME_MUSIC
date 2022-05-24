from pyrogram import Client, filters
from pyrogram.types import Message

from FlameMusic import SUDOERS, app
from FlameMusic.FlameMusicUtilities.database.auth import (_get_authusers, delete_authuser, get_authuser,
                            get_authuser_count, get_authuser_names,
                            save_authuser)
from FlameMusic.FlameMusicUtilities.helpers.admins import AdminActual
from FlameMusic.FlameMusicUtilities.database.changers import (alpha_to_int, int_to_alpha,
                                      time_to_seconds)


@app.on_message(filters.command("auth") & filters.group)
@AdminActual
async def auth(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Rᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        user_id = message.from_user.id
        token = await int_to_alpha(user.id)
        from_user_name = message.from_user.first_name
        from_user_id = message.from_user.id
        _check = await get_authuser_names(message.chat.id)
        count = 0
        for smex in _check:
            count += 1
        if int(count) == 20:
            return await message.reply_text(
                "Yᴏᴜ ᴄᴀɴ ᴏɴʟʏ ʜᴀᴠᴇ 20 Usᴇʀs Iɴ Yᴏᴜʀ Gʀᴏᴜᴘs Aᴜᴛʜᴏʀɪsᴇᴅ Usᴇʀs Lɪsᴛ (AUL)"
            )
        if token not in _check:
            assis = {
                "auth_user_id": user.id,
                "auth_name": user.first_name,
                "admin_id": from_user_id,
                "admin_name": from_user_name,
            }
            await save_authuser(message.chat.id, token, assis)
            await message.reply_text(
                f"Aᴅᴅᴇᴅ ᴛᴏ Aᴜᴛʜᴏʀɪsᴇᴅ Usᴇʀs Lɪsᴛ ᴏғ ᴛʜɪs ɢʀᴏᴜᴘ."
            )
            return
        else:
            await message.reply_text(f"Aʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇ Aᴜᴛʜᴏʀɪsᴇᴅ Usᴇʀs Lɪsᴛ.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    token = await int_to_alpha(user_id)
    from_user_name = message.from_user.first_name
    _check = await get_authuser_names(message.chat.id)
    count = 0
    for smex in _check:
        count += 1
    if int(count) == 20:
        return await message.reply_text(
            "Yᴏᴜ ᴄᴀɴ ᴏɴʟʏ ʜᴀᴠᴇ 20 Usᴇʀs Iɴ Yᴏᴜʀ Gʀᴏᴜᴘs Aᴜᴛʜᴏʀɪsᴇᴅ Usᴇʀs Lɪsᴛ (AUL)"
        )
    if token not in _check:
        assis = {
            "auth_user_id": user_id,
            "auth_name": user_name,
            "admin_id": from_user_id,
            "admin_name": from_user_name,
        }
        await save_authuser(message.chat.id, token, assis)
        await message.reply_text(
            f"Aᴅᴅᴇᴅ ᴛᴏ Aᴜᴛʜᴏʀɪsᴇᴅ Usᴇʀs Lɪsᴛ ᴏғ ᴛʜɪs ɢʀᴏᴜᴘ."
        )
        return
    else:
        await message.reply_text(f"Aʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇ Aᴜᴛʜᴏʀɪsᴇᴅ Usᴇʀs Lɪsᴛ.")


@app.on_message(filters.command("unauth") & filters.group)
@AdminActual
async def whitelist_chat_func(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Reply to a user's message or give username/user_id."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        token = await int_to_alpha(user.id)
        deleted = await delete_authuser(message.chat.id, token)
        if deleted:
            return await message.reply_text(
                f"Removed  ᴛᴏ Aᴜᴛʜᴏʀɪsᴇᴅ Usᴇʀs Lɪsᴛ ᴏғ ᴛʜɪs ɢʀᴏᴜᴘ."
            )
        else:
            return await message.reply_text(f"Not an Authorised User.")
    user_id = message.reply_to_message.from_user.id
    token = await int_to_alpha(user_id)
    deleted = await delete_authuser(message.chat.id, token)
    if deleted:
        return await message.reply_text(
            f"Removed ᴛᴏ Aᴜᴛʜᴏʀɪsᴇᴅ Usᴇʀs Lɪsᴛ ᴏғ ᴛʜɪs ɢʀᴏᴜᴘ."
        )
    else:
        return await message.reply_text(f"Not an Authorised User.")


@app.on_message(filters.command("authusers") & filters.group)
async def authusers(_, message: Message):
    _playlist = await get_authuser_names(message.chat.id)
    if not _playlist:
        return await message.reply_text(
            f"Nᴏ Aᴜᴛʜᴏʀɪsᴇᴅ Usᴇʀs ɪɴ ᴛʜɪs Gʀᴏᴜᴘ.\ɴ\ɴAᴅᴅ Aᴜᴛʜ ᴜsᴇʀs ʙʏ /auth ᴀɴᴅ ʀᴇᴍᴏᴠᴇ ʙʏ /unauth."
        )
    else:
        j = 0
        m = await message.reply_text(
            "Fᴇᴛᴄʜɪɴɢ Aᴜᴛʜᴏʀɪsᴇᴅ Usᴇʀs... Pʟᴇᴀsᴇ Wᴀɪᴛ"
        )
        msg = f"**Aᴜᴛʜᴏʀɪsᴇᴅ Usᴇʀs Lɪsᴛ[AUL]:**\n\n"
        for note in _playlist:
            _note = await get_authuser(message.chat.id, note)
            user_id = _note["auth_user_id"]
            user_name = _note["auth_name"]
            admin_id = _note["admin_id"]
            admin_name = _note["admin_name"]
            try:
                user = await app.get_users(user_id)
                user = user.first_name
                j += 1
            except Exception:
                continue
            msg += f"{j}➤ {user}[`{user_id}`]\n"
            msg += f"    ┗ 🇦ᴅᴅᴇᴅ ʙʏ :- {admin_name}[`{admin_id}`]\n\n"
        