import asyncio

from FlameMusic import BOT_ID, OWNER, app
from FlameMusic.FlameMusicUtilities.database.chats import get_served_chats
from FlameMusic.FlameMusicUtilities.database.gbanned import (
    add_gban_user,
    is_gbanned_user,
    remove_gban_user,
)
from FlameMusic.FlameMusicUtilities.database.sudo import get_sudoers
from pyrogram import filters
from pyrogram.errors import FloodWait


@app.on_message(filters.command("gban") & filters.user(OWNER))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**Consumption:**\n/block [USERNAME | USER_ID]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            return await message.reply_text("You want to block yourself?")
        elif user.id == BOT_ID:
            await message.reply_text("Should I block myself??")
        elif user.id in sudoers:
            await message.reply_text("You want to block a sudo user?")
        else:

            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"""
**Initialize Global Ban on {user.mention}**

Expected time: {len(served_chats)}
"""
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**New Global Ban on Music**__
**Reason:** {message.chat.title} [`{message.chat.id}`]
**sudo user:** {from_user.mention}
**Blocked Users:** {user.mention}
**Blocked User ID:** `{user.id}`
**chat:** {number_of_chats}
"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("You want to block yourself?")
    elif user_id == BOT_ID:
        await message.reply_text("Should I block myself??")
    elif user_id in sudoers:
        await message.reply_text("You want to block a sudo user?")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("Already Gbanned.")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"""
**Initialize Global Ban on {mention}**

Expected time: {len(served_chats)}
"""
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**New Global Ban on Music**__
**reason:** {message.chat.title} [`{message.chat.id}`]
** Sudo user:** {from_user_mention}
**blocked sudo users:** {mention}
**Chat User ID:** `{user_id}`
**Chats:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("ungban") & filters.user(OWNER))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("**user:**\n/unblock [USERNAME | USER_ID]")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            await message.reply_text("You wanna block urself?")
        elif user.id == BOT_ID:
            await message.reply_text("Should I unblock myself??")
        elif user.id in sudoers:
            await message.reply_text("Sudo users can't be blocked/blocked.")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("He is already free, why bully him?")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"Ungbanned!")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("you wanna block urself?")
    elif user_id == BOT_ID:
        await message.reply_text(
            "Should I unblock myself? But I'm not blocked."
        )
    elif user_id in sudoers:
        await message.reply_text("Sudo users can't be blocked/blocked.")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("He is already free, why bully him?")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"Ungbanned!")


chat_watcher_group = 5


@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    try:
        userid = message.from_user.id
    except Exception:
        return
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.kick_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"""
{checking} is globally banned by Music and has been removed from the chat.

**Possible Reasons:** Potential Spammers and Abusers.
"""
    )
