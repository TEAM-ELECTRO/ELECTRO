# Copyright (C) 2019 The Rphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
"""
Userbot module to help you manage a group
"""

from asyncio import sleep

from telethon import functions
from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)

from userbot import *
from userbot.plugins.sql_helper.mute_sql import is_muted, mute, unmute
from ElectroBot.utils import *
from userbot.cmdhelp import CmdHelp

# =================== CONSTANT ===================

PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "`I am not an admin! Chutiya sala`"
NO_PERM = "`I don't have sufficient permissions! Sed -_-`"
CHAT_PP_CHANGED = "`Chat Picture Changed Successfully`"
INVALID_MEDIA = "`Invalid media Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

# ================================================


@bot.on(admin_cmd("setgpic$"))
@bot.on(sudo_cmd(pattern="setgpic$", allow_sudo=True))
@errors_handler
async def set_group_photo(gpic):
    if gpic.fwd_from:
        return
    if not gpic.is_group:
        await edit_or_reply(gpic, "`I don't think this is a group.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None
    if not admin and not creator:
        await edit_or_reply(gpic, NO_ADMIN)
        return
    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await edit_or_reply(gpic, INVALID_MEDIA)
    aura = None
    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            await edit_or_reply(gpic, CHAT_PP_CHANGED)
            aura = True
        except PhotoCropSizeSmallError:
            await edit_or_reply(gpic, PP_TOO_SMOL)
        except ImageProcessFailedError:
            await edit_or_reply(gpic, PP_ERROR)
        except Exception as e:
            await edit_or_reply(gpic, f"**Error : **`{str(e)}`")
        if BOTLOG and aura:
            await gpic.client.send_message(
                BOTLOG_CHATID,
                "#GROUPPIC\n"
                f"Group profile pic changed "
                f"CHAT: {gpic.chat.title}(`{gpic.chat_id}`)",
            )


@bot.on(admin_cmd("promote(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="promote(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def promote(promt):
    if promt.fwd_from:
        return
    chat = await promt.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(promt, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    Electroevent = await edit_or_reply(promt, "Promoting...")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "Electro"
    if not user:
        return
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await Electroevent.edit("𝙋𝙍𝙊𝙈𝙊𝙏𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔..!!")
    except BadRequestError:
        await Electroevent.edit(NO_PERM)
        return
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)",
        )


@bot.on(admin_cmd("demote(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="demote(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def demote(dmod):
    if dmod.fwd_from:
        return
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(dmod, NO_ADMIN)
        return
    Electroevent = await edit_or_reply(dmod, "Demoting...")
    rank = "??????"
    user = await get_user_from_event(dmod)
    user = user[0]
    if not user:
        return
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))
    except BadRequestError:
        await Electroevent.edit(NO_PERM)
        return
    await Electroevent.edit("𝘿𝙀𝙈𝙊𝙏𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔..!!")
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID,
            "#DEMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)",
        )


@bot.on(admin_cmd("ban(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="ban(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def ban(bon):
    if bon.fwd_from:
        return
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(bon, NO_ADMIN)
        return
    user, reason = await get_user_from_event(bon)
    if not user:
        return
    Electroevent = await edit_or_reply(bon, "Banning this retard")
    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await Electroevent.edit(NO_PERM)
        return
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await Electroevent.edit("𝙄 𝙖𝙞𝙣'𝙩 𝙜𝙤𝙩 𝙢𝙨𝙜 𝙙𝙚𝙡𝙚𝙩𝙞𝙣𝙜 𝙧𝙞𝙜𝙝𝙩. 𝘽𝙪𝙩 𝙨𝙩𝙞𝙡𝙡 𝘽𝙖𝙣𝙣𝙚𝙙!")
        return
    if reason:
        await Electroevent.edit(f"{str(user.id)} 𝙄𝙎 𝘽𝘼𝙉𝙉𝙀𝘿...!!\nReason: {reason}")
    else:
        await Electroevent.edit(f"{str(user.id)} 𝙄𝙎 𝘽𝘼𝙉𝙉𝙀𝘿...!!")
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {bon.chat.title}({bon.chat_id})",
        )


@bot.on(admin_cmd("unban(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="unban(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def nothanos(unbon):
    if unbon.fwd_from:
        return
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(unbon, NO_ADMIN)
        return
    Electroevent = await edit_or_reply(unbon, "Unbanning...")
    user = await get_user_from_event(unbon)
    user = user[0]
    if not user:
        return
    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await Electroevent.edit("𝙐𝙉𝘽𝘼𝙉𝙉𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 𝙃𝙊𝙋𝙀 𝙔𝙊𝙐 𝙃𝘼𝙑𝙀 𝙇𝙀𝘼𝙍𝙉𝙀𝘿 𝘼 𝙇𝙀𝙎𝙎𝙊𝙉...!!")
        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)",
            )
    except UserIdInvalidError:
        await Electroevent.edit("𝙎𝙤𝙧𝙧𝙮 𝙄 𝘾𝙖𝙣'𝙩 𝙐𝙣𝙗𝙖𝙣 𝙏𝙝𝙞𝙨 𝙍𝙚𝙩𝙖𝙧𝙙!")


@command(incoming=True)
async def watcher(event):
    if event.fwd_from:
        return
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))

@bot.on(admin_cmd("pin($| (.*))"))
@bot.on(sudo_cmd(pattern="pin($| (.*))", allow_sudo=True))
@errors_handler
async def pin(msg):
    if msg.fwd_from:
        return
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(msg, NO_ADMIN)
        return
    to_pin = msg.reply_to_msg_id
    if not to_pin:
        await edit_or_reply(msg, "𝙍𝙚𝙥𝙡𝙮 𝙩𝙤 𝙖 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙩𝙤 𝙥𝙞𝙣 𝙞𝙩.")
        return
    options = msg.pattern_match.group(1)
    is_silent = True
    if options.lower() == "loud":
        is_silent = False
    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await edit_or_reply(msg, NO_PERM)
        return
    hmm = await edit_or_reply(msg, "𝙋𝙄𝙉𝙉𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔...!!")
    user = await get_user_from_id(msg.sender_id, msg)
    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID,
            "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}",
        )
    await sleep(3)
    try:
        await hmm.delete()
    except:
        pass


@bot.on(admin_cmd("kick(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="kick(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def kick(usr):
    if usr.fwd_from:
        return
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(usr, NO_ADMIN)
        return
    user, reason = await get_user_from_event(usr)
    if not user:
        await edit_or_reply(usr, "𝘾𝙤𝙪𝙡𝙙𝙣'𝙩 𝙛𝙚𝙩𝙘𝙝 𝙪𝙨𝙚𝙧.")
        return
    Electroevent = await edit_or_reply(usr, "Kicking...")
    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await Electroevent.edit(NO_PERM + f"\n{str(e)}")
        return
    if reason:
        await Electroevent.edit(
            f"𝙆𝙄𝘾𝙆𝙀𝘿 [{user.first_name}](tg://user?id={user.id})!\nReason: {reason}"
        )
    else:
        await Electroevent.edit(f"𝙆𝙄𝘾𝙆𝙀𝘿 [{user.first_name}](tg://user?id={user.id})!")
    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {usr.chat.title}({usr.chat_id})\n",
        )


@bot.on(admin_cmd("undlt$"))
@bot.on(sudo_cmd(pattern="undlt$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.fwd_from:
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await event.client.get_admin_log(
            event.chat_id, limit=5, edit=False, delete=True
        )
        deleted_msg = "𝘿𝙚𝙡𝙚𝙩𝙚𝙙 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙞𝙣 𝙩𝙝𝙞𝙨 𝙜𝙧𝙤𝙪𝙥:"
        for i in a:
            deleted_msg += "\n👉{}".format(i.old.message)
        await edit_or_reply(event, deleted_msg)
    else:
        await edit_or_reply(
            event, "𝙔𝙤𝙪 𝙣𝙚𝙚𝙙 𝙖𝙙𝙢𝙞𝙣𝙞𝙨𝙩𝙧𝙖𝙩𝙞𝙫𝙚 𝙥𝙚𝙧𝙢𝙞𝙨𝙨𝙞𝙤𝙣𝙨 𝙞𝙣 𝙤𝙧𝙙𝙚𝙧 𝙩𝙤 𝙙𝙤 𝙩𝙝𝙞𝙨 𝙘𝙤𝙢𝙢𝙖𝙣𝙙"
        )
        await sleep(3)
        try:
            await event.delete()
        except:
            pass


async def get_user_from_event(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("𝙋𝙖𝙨𝙨 𝙩𝙝𝙚 𝙪𝙨𝙚𝙧'𝙨 𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚, 𝙞𝙙 𝙤𝙧 𝙧𝙚𝙥𝙡𝙮!")
            return
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await event.edit("𝘾𝙤𝙪𝙡𝙙 𝙣𝙤𝙩 𝙛𝙚𝙩𝙘𝙝 𝙞𝙣𝙛𝙤 𝙤𝙛 𝙩𝙝𝙖𝙩 𝙪𝙨𝙚𝙧.")
            return None
    return user_obj, extra


async def get_user_from_id(user, event):
    if event.fwd_from:
        return
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj

CmdHelp("admin").add_command(
       'setgpic', '<reply to image>', 'Changes the groups display picture'
).add_command(
        'promote', '<username/reply> <custom rank (optional)>',
        'Provides admins right to a person in the chat.'
).add_command(
        'demote', '<username/reply>', 'Revokes the person admin permissions    in the chat.'
).add_command(
        'ban', '<username/reply> <reason (optional)>', 'Bans the person off your chat.'
).add_command(
        'unban', '<username/reply>', 'Removes the ban from the person in the chat.'
).add_command(
        'mute', '<username/reply> <reason (optional)>', 'Mutes the person in the chat, works on admins too.'
).add_command(
        'unmute', '<username/reply>', 'Removes the person from the muted list.'
).add_command(
        'pin', '<reply> or .pin loud', 'Pins the replied message in Group'
).add_command(
        'kick', '<username/reply>', 'kick the person off your chat'
).add_command(
        'iundlt', None, 'display last 5 deleted messages in group.'
).add()
