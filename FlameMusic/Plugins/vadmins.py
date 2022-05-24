from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from FlameMusic import app
from FlameMusic.FlameMusicUtilities.tgcallsrun.music import pytgcalls as call_py

from FlameMusic.FlameMusicUtilities.helpers.decorators import authorized_users_only
from FlameMusic.FlameMusicUtilities.helpers.filters import command
from FlameMusic.FlameMusicUtilities.tgcallsrun.queues import QUEUE, clear_queue
from FlameMusic.FlameMusicUtilities.tgcallsrun.video import skip_current_song, skip_item


bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup([[InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="cls")]])


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "ʏᴏᴜ ᴀʀᴇ **ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ** !\n\n» ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ғʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛs."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 ᴏɴʟʏ ᴀᴅᴍɪɴs ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏn  !",
            show_alert=True,
        )
    await query.edit_message_text(
        f"⚙️ **sᴇᴛᴛɪɴɢs ᴏғ** {query.message.chat.title}\n\nII : ᴘᴀᴜsᴇ Streaming\n▷ : ᴄᴏɴᴛɪɴᴜᴇ Streaming\n🔇 : sᴄʀᴇᴡ ғᴇᴇʟɪɴɢ       Assistant\n🔊 : ʀɪɴɢ ɪᴛ Assistant\n▢ : sᴛᴏᴘ sᴛʀᴇᴀᴍɪɴɢ",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("▢", callback_data="cbstop"),
                    InlineKeyboardButton("II", callback_data="cbpause"),
                    InlineKeyboardButton("▷", callback_data="cbresume"),
                ],
                [
                    InlineKeyboardButton("🔇", callback_data="cbmute"),
                    InlineKeyboardButton("🔊", callback_data="cbunmute"),
                ],
                [InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="cls")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 ᴏɴʟʏ ᴀᴅᴍɪɴs ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ !",
            show_alert=True,
        )
    await query.message.delete()


@app.on_message(command(["vskip"]) & filters.group)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴍᴇɴᴜ", callback_data="cbmenu"),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ")
        elif op == 1:
            await m.reply(
                "✅ __ϙᴜᴇᴜᴇ__ **ᴇᴍᴘᴛʏ.**\n\n**• ᴀssɪsᴛᴀɴᴛ ʟᴇғᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ**"
            )
        elif op == 2:
            await m.reply(
                "🗑️ **ᴄʟᴇᴀʀɪɴɢ ᴛʜᴇ ϙᴜᴇᴜᴇ**\n\n**• ᴀssɪsᴛᴀɴᴛ ʟᴇᴀᴠᴇs ᴠᴏɪᴄᴇ ᴄʜᴀᴛ**"
            )
        else:
            await m.reply(
                f"""
⏭️ **ᴛᴡɪsᴛ {op[2]} ɴᴇxᴛ**

🏷 **Nama:** [{op[0]}]({op[1]})
🎧 **Atas permintaan:** {m.from_user.mention()}
""",
                disable_web_page_preview=True,
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **sᴏɴɢ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ϙᴜᴇᴜᴇ:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@app.on_message(command(["vstop"]) & filters.group)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ **ᴛʜᴇ sᴛʀᴇᴀᴍ ʜᴀs ᴇɴᴅᴇᴅ.**")
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛ ɪɴ sᴛʀᴇᴀᴍ**")


@app.on_message(command(["vpause"]) & filters.group)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "II **ᴠɪᴅᴇᴏ ɪs ᴘᴀᴜsᴇᴅ.**\n\n• **ᴛᴏ ʀᴇsᴜᴍᴇ ᴠɪᴅᴇᴏ, ᴜsᴇ ᴄᴏᴍᴍᴀɴᴅ** » /vresume"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **noᴛ ɪɴ sᴛʀᴇᴀᴍ**")


@app.on_message(command(["vresume"]) & filters.group)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▷ **Vᴠɪᴅᴇᴏ ʀᴇsᴜᴍᴇs.**\n\n• **ᴛᴏ ᴘᴀᴜsᴇ ᴛʜᴇ ᴠɪᴅᴇᴏ, ᴜsᴇ ᴄᴏᴍᴍᴀɴᴅ** » /vpause"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛ ɪɴ sᴛʀᴇᴀᴍ**")


@app.on_message(command(["vmute"]) & filters.group)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 **ᴀssɪsᴛᴀɴᴛ ɪs ᴍᴜᴛᴇᴅ. ** \n\n• ** ᴛᴏ ᴀᴄᴛɪᴠᴀᴛᴇ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴠᴏɪᴄᴇ, ᴜsᴇ ᴄᴏᴍᴍᴀɴᴅs**\n» /vunmute"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛ ɪɴ sᴛʀᴇᴀᴍ**")


@app.on_message(command(["vunmute"]) & filters.group)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 **ᴀssɪsᴛᴀɴᴛ ɪs ᴀᴄᴛɪᴠᴀᴛᴇᴅ.**\ɴ\ɴ• **ᴛᴏ ᴅɪsᴀʙʟᴇ ᴜsᴇʀ ʙᴏᴛs, ᴜsᴇ ᴄᴏᴍᴍᴀɴᴅ**\n» /vmute"
            )
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛ ɪɴ sᴛʀᴇᴀᴍ**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "ʏᴏᴜ ᴀʀᴇ **ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ** !\n\n» ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ғʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛs."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 ᴏɴʟʏ ᴀᴅᴍɪɴs ᴡɪᴛʜ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴍᴀɴᴀɢᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ!!",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text("II ᴛʜᴇ sᴛʀᴇᴀᴍ ʜᴀs ʙᴇᴇɴ ᴘᴀᴜsᴇᴅ", reply_markup=bttn)
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ɴᴏᴛʜɪɴɢ ɪs ɢᴏɪɴɢ ᴏɴ ", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "ʏᴏᴜ ᴀʀᴇ **ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ** !\n\n» ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ғʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛs.."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 ᴏɴʟʏ ᴀᴅᴍɪɴs ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ !",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "▷ Stʀᴇᴀᴍɪɴɢ ʜᴀs ʀᴇsᴜᴍᴇᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "ʏᴏᴜ ᴀʀᴇ **ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ** !\n\n» ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ғʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛs."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 ᴏɴʟʏ ᴀᴅᴍɪɴs ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ !",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text(
                "✅ **ᴛʜᴇ sᴛʀᴇᴀᴍ ʜᴀs ᴇɴᴅᴇᴅ**", reply_markup=bcl
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ɴᴏᴛʜɪɴɢ ɪs sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "ʏᴏᴜ ᴀʀᴇ **ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ** !\n\n» ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ғʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛs."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 ᴏɴʟʏ ᴀᴅᴍɪɴs ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏn !",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 Assistant Succesfully joined", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"***Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "ʏᴏᴜ ᴀʀᴇ **ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ** !\ɴ\ɴ» ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ғʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛs."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "💡 ᴏɴʟʏ ᴀᴅᴍɪɴs ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ !",
            show_alert=True,
        )
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 ᴀssɪsᴛᴀɴᴛ sᴏᴜɴᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"**Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌  ɴᴏ ᴏɴᴇ ɪs sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@app.on_message(command(["volume", "vol"]))
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(f"✅ **Volume disetel ke** `{range}`%")
        except Exception as e:
            await m.reply(f"**Error:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛ ɪɴ sᴛʀᴇᴀᴍ**")
