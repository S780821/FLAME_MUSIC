import asyncio
import yt_dlp
import psutil

from FlameMusic.config import GROUP, CHANNEL
from FlameMusic import (
    ASSID,
    BOT_ID,
    BOT_NAME,
    BOT_USERNAME,
    OWNER,
    SUDOERS,
    app,
)
from FlameMusic.FlameMusicUtilities.database.chats import is_served_chat
from FlameMusic.FlameMusicUtilities.database.queue import remove_active_chat
from FlameMusic.FlameMusicUtilities.database.sudo import get_sudoers
from FlameMusic.FlameMusicUtilities.database.assistant import (_get_assistant, get_as_names, get_assistant,
                        save_assistant)
from FlameMusic.FlameMusicUtilities.database.auth import (_get_authusers, add_nonadmin_chat, delete_authuser,
                   get_authuser, get_authuser_count, get_authuser_names,
                   is_nonadmin_chat, remove_nonadmin_chat, save_authuser)
from FlameMusic.FlameMusicUtilities.database.blacklistchat import blacklist_chat, blacklisted_chats, whitelist_chat
from FlameMusic.FlameMusicUtilities.helpers.admins import ActualAdminCB
from FlameMusic.FlameMusicUtilities.helpers.inline import personal_markup, setting_markup
from FlameMusic.FlameMusicUtilities.helpers.inline import (custommarkup, dashmarkup, setting_markup,
                          start_pannel, usermarkup, volmarkup)
from FlameMusic.FlameMusicUtilities.helpers.thumbnails import down_thumb
from FlameMusic.FlameMusicUtilities.helpers.ytdl import ytdl_opts
from FlameMusic.FlameMusicUtilities.tgcallsrun.music import pytgcalls
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


def start_pannel():
    buttons = [
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ​", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/Flame_Updates"),
        ],
        [
            InlineKeyboardButton("📚 ᴄᴏᴍᴍᴀɴᴅ​ 📚", url="https://t.me/Flame_Updates/2"),
        ],
        [
            InlineKeyboardButton("🌐 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ 🌐", url="https://github.com/S780821/Flame_Music"),
        ],
    ]
    return (
        "🎛 **{BOT_NAME} ɪs ᴏɴᴇ ᴏғ ᴛʜᴇ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛs ᴛʜᴀᴛ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ɢʀᴏᴜᴘs**",
        buttons,
    )


pstart_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ​", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/Flame_Updates"),
        ],
        [
            InlineKeyboardButton("📚 ᴄᴏᴍᴍᴀɴᴅ ​📚", url="https://t.me/Flame_Updates/2"),
        ],
        [
            InlineKeyboardButton("🌐 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ 🌐", url="https://github.com/S780821/Flame_Music"),
        ],
    ]
)
welcome_captcha_group = 2


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await message.reply_text(
                    f"💡 ʙᴏᴛ ᴏᴡɴᴇʀ [{member.mention}] baru saja bergabung di grup ini."
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"💡 Admin Bot [{member.mention}] ᴊᴜsᴛ ᴊᴏɪɴᴇᴅ ᴛʜɪs ɢʀᴏᴜᴘ."
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(
                    f"""
👋 ** ʜᴇʟʟᴏ, ɪᴛ's ɴɪᴄᴇ ᴛᴏ ʙᴇ ᴀʙʟᴇ ᴛᴏ ᴊᴏɪɴ ᴛʜɪs ɢʀᴏᴜᴘ**

💡 **ᴅᴏɴ'ᴛ ғᴏʀɢᴇᴛ ᴛᴏ ᴍᴀᴋᴇ ᴍᴇ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ**
""",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                    disable_web_page_preview=True
                )
                return
        except BaseException:
            return


@Client.on_message(
    filters.group
    & filters.command(
        ["start", "help", f"start@{BOT_USERNAME}", f"help@{BOT_USERNAME}"]
    )
)
async def start(_, message: Message):
    chat_id = message.chat.id
    out = start_pannel()
    await message.reply_text(
        f"""
ᴛʜᴀɴᴋs ғᴏʀ ᴘᴜᴛᴛɪɴɢ ᴍᴇ ɪɴ {message.chat.title}.
ᴍᴜsɪᴄ ɪs ᴀʟɪᴠᴇ.

ғᴏʀ ʜᴇʟᴘ ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ.
""",
        reply_markup=InlineKeyboardMarkup(out[1]),
        disable_web_page_preview=True
    )
    return


@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await app.send_message(
            message.chat.id,
            text=f"""
**✨ ᴡᴇʟᴄᴏᴍᴇ {rpk}!

💬 [{BOT_NAME}](tg://user?id=2129034376) ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ɢʀᴏᴜᴘs ᴠɪᴀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴡʜɪᴄʜ ɪs ɴᴇᴡ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ!

💡 ᴛᴏ ᴋɴᴏᴡ ᴀʟʟ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ʜᴏᴡ ɪᴛ ᴡᴏʀᴋs ᴡɪᴛʜ ᴛʜᴇ ᴘʀᴇss ᴏғ ᴀ ʙᴜᴛᴛᴏɴ.» 📚 ᴄᴏᴍᴍᴀɴᴅ​!**

""",
            parse_mode="markdown",
            reply_markup=pstart_markup,
            reply_to_message_id=message.message_id,
        )
    elif len(message.command) == 2:
        query = message.text.split(None, 1)[1]
        f1 = query[0]
        f2 = query[1]
        f3 = query[2]
        finxx = f"{f1}{f2}{f3}"
        if str(finxx) == "inf":
            query = (str(query)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                x = ytdl.extract_info(query, download=False)
            thumbnail = x["thumbnail"]
            searched_text = f"""
🔍 **Video Track Information**

❇️**🇹ɪᴛʟᴇ:** {x["title"]}

⏳ **🇩ᴜʀᴀᴛɪᴏɴ:** {round(x["duration"] / 60)} Mins
👀 **🇵ᴏsɪᴛɪᴏɴ:** `{x["view_count"]}`
👍 **ᴛʜᴇʏ:** `{x["like_count"]}`
👎 **ᴅᴏ ɴᴏᴛ ʟɪᴋᴇ:** `{x["dislike_count"]}`
⭐️ **ᴀᴠᴇʀᴀɢᴇ ʀᴀᴛɪɴg:** {x["average_rating"]}
🎥 **🇳ᴀᴍᴇ channel:** {x["uploader"]}
📎 **🇨ʜᴀɴɴᴇʟ Link:** [Kunjungi Dari Sini]({x["channel_url"]})
🔗 **Link:** [Link]({x["webpage_url"]})
"""
            link = x["webpage_url"]
            buttons = personal_markup(link)
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await app.send_photo(
                message.chat.id,
                photo=thumb,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if str(finxx) == "sud":
            sudoers = await get_sudoers()
            text = "**📝 sᴜᴅᴏ ᴜsᴇʀ ʟɪsᴛ**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue
                text += f"- {user}\n"
            if not text:
                await message.reply_text("ɴᴏ sᴜᴅᴏ ᴜsᴇʀ")
            else:
                await message.reply_text(text)


@app.on_message(filters.command("settings") & filters.group)
async def settings(_, message: Message):
    c_id = message.chat.id
    _check = await get_assistant(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_assistant(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    text, buttons = setting_markup()
    await asyncio.gather(
        message.delete(),
        message.reply_text(f"{text}\n\n**Group:** {message.chat.title}\n**Group ID:** {message.chat.id}\n**Volume Level:** {volume}%", reply_markup=InlineKeyboardMarkup(buttons)),
    )

@app.on_callback_query(filters.regex("okaybhai"))
async def okaybhai(_, CallbackQuery):
    await CallbackQuery.answer("Going Back ...")
    out = start_pannel()
    await CallbackQuery.edit_message_text(
        text=f"ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ᴏɴ {CallbackQuery.message.chat.title}.\n{BOT_NAME} ᴀʟʀᴇᴀᴅʏ ᴏɴʟɪɴe.\n\nɪғ ʏᴏᴜ ɴᴇᴇᴅ ʜᴇʟᴘ ᴏʀ ᴛʜᴇʀᴇ ɪs ᴀ ᴘʀᴏʙʟᴇᴍ ᴡɪᴛʜ ᴛʜᴇ ʙᴏᴛ, ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀ ᴄʜᴀɴɴᴇʟ.",
        reply_markup=InlineKeyboardMarkup(out[1]),
    )

@app.on_callback_query(filters.regex("settingm"))
async def settingm(_, CallbackQuery):
    await CallbackQuery.answer("Bot Settings ...")
    text, buttons = setting_markup()
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    _check = await get_assistant(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_assistant(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    await CallbackQuery.edit_message_text(
        text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@app.on_callback_query(filters.regex("EVE"))
@ActualAdminCB
async def EVE(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer("Changes Saved")
        await add_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nAdmins Commands Mode to **Everyone**\n\nNow anyone present in this group can skip, pause, resume, stop music.\n\nChanges Done By @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await CallbackQuery.answer(
            "Commands Mode is Already Set To EVERYONE", show_alert=True
        )

@app.on_callback_query(filters.regex("AMS"))
@ActualAdminCB
async def AMS(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer(
            "Commands Mode is Already Set To ADMINS ONLY", show_alert=True
        )
    else:
        await CallbackQuery.answer("Changes Saved")
        await remove_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nSet Commands Mode to **Admins**\n\nNow only Admins present in this group can skip, pause, resume, stop musics.\n\nChanges Done By @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(AQ|AV|AU|Dashboard|HV|LV|MV|HV|VAM|Custommarkup|PTEN|MTEN|PTF|MTF|PFZ|MFZ|USERLIST|UPT|CPT|RAT|DIT)$"
    )
)
async def start_markup_check(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    if command == "AQ":
        await CallbackQuery.answer("Already in Best Quality", show_alert=True)
    if command == "AV":
        await CallbackQuery.answer("Bot Settings ...")
        text, buttons = volmarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "AU":
        await CallbackQuery.answer("Bot Settings ...")
        text, buttons = usermarkup()
        is_non_admin = await is_nonadmin_chat(chat_id)
        if not is_non_admin:
            current = "Admins Only"
        else:
            current = "Everyone"
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n\nCurrently Who Can Use {BOT_NAME}:- **{current}**\n\n**⁉️ What is This?**\n\n**👥 Everyone :-**Anyone can use {BOT_NAME}'s commands(skip, pause, resume etc) present in this group.\n\n**🙍 Admin Only :-**  Only the admins and authorized users can use all commands of {BOT_NAME}.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Dashboard":
        await CallbackQuery.answer("Dashboard...")
        text, buttons = dashmarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n\nCheck {BOT_NAME}'s System Stats In the DashBoard Here! More Functions adding very soon! Keep on Checking Support Channel.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Custommarkup":
        await CallbackQuery.answer("Bot Settings ...")
        text, buttons = custommarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "LV":
        assis = {
            "volume": 25,
        }
        volume = 25
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MV":
        assis = {
            "volume": 50,
        }
        volume = 50
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "HV":
        assis = {
            "volume": 100,
        }
        volume = 100
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "VAM":
        assis = {
            "volume": 200,
        }
        volume = 200
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "USERLIST":
        await CallbackQuery.answer("Auth Users!")
        text, buttons = usermarkup()
        _playlist = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.edit_message_text(
                text=f"{text}\n\nNo Authorized Users Found\n\nYou can allow any non-admin to use my admin commands by /auth and delete by using /unauth",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            j = 0
            await CallbackQuery.edit_message_text(
                "Fetching Authorised Users... Please Wait"
            )
            msg = f"**Authorised Users List[AUL]:**\n\n"
            for note in _playlist:
                _note = await get_authuser(
                    CallbackQuery.message.chat.id, note
                )
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
                msg += f"    ┗ Added By:- {admin_name}[`{admin_id}`]\n\n"
            await CallbackQuery.edit_message_text(
                msg, reply_markup=InlineKeyboardMarkup(buttons)
            )
    if command == "UPT":
        bot_uptimee = int(time.time() - bot_start_time)
        Uptimeee = f"{get_readable_time((bot_uptimee))}"
        await CallbackQuery.answer(
            f"Bot's Uptime: {Uptimeee}", show_alert=True
        )
    if command == "CPT":
        cpue = psutil.cpu_percent(interval=0.5)
        await CallbackQuery.answer(
            f"Bot's Cpu Usage: {cpue}%", show_alert=True
        )
    if command == "RAT":
        meme = psutil.virtual_memory().percent
        await CallbackQuery.answer(
            f"Bot's Memory Usage: {meme}%", show_alert=True
        )
    if command == "DIT":
        diske = psutil.disk_usage("/").percent
        await CallbackQuery.answer(
            f"Disk Usage: {diske}%", show_alert=True
        )
