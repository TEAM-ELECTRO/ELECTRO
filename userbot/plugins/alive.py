import time
from userbot import *
from ElectroBot.utils import *
from userbot.cmdhelp import CmdHelp
from telethon import events, version
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon import version
from userbot import ALIVE_NAME, StartTime, Electroversion
from ElectroBot.utils import admin_cmd, edit_or_reply, sudo_cmd


#-------------------------------------------------------------------------------


async def reply_id(event):
    reply_to_id = None
    if event.sender_id in Config.SUDO_USERS:
        reply_to_id = event.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    return reply_to_id

ludosudo = Config.SUDO_USERS
if ludosudo:
    sudou = "True"
else:
    sudou = "False"

DEFAULTUSER = ALIVE_NAME or "Electro User"
Electro_IMG = Config.ALIVE_PIC
CUSTOM_ALIVE_TEXT = Config.ALIVE_MSG or "Legendary ElectroBot"

USERID = bot.uid

mention = f"[{DEFAULTUSER}](tg://user?id={USERID})"


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


uptime = get_readable_time((time.time() - StartTime))


@bot.on(admin_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    reply_to_id = await reply_id(alive)

    if Electro_IMG:
        Electro_caption = f"**{CUSTOM_ALIVE_TEXT}**\n\n"
        
        Electro_caption += f"      __**╚»★BOT INFO★«╝**__\n"
        Electro_caption += f"**╭────────☆═━┈┈┈━═☆───────╮**\n"
        Electro_caption += f"**※┄┄➳ BOT OWNER:** ** {mention} **\n"
        Electro_caption += f"**※┄┄➳ BOT STATUS : WORKING NORMALLY **\n"
        Electro_caption += f"**※┄┄➳ YOUR BOT VERSION :**`{Electroversion}`\n"
        Electro_caption += f"**※┄┄➳ SECURITY STATUS : NO BUGS **\n"
        Electro_caption += f"**※┄┄➳ TELETHON VERSION : ** `{version.__version__}`\n"
        Electro_caption += f"**※┄┄➳ UPTIME :** `{uptime}`\n"
        Electro_caption += f"**※┄┄➳ SUDO STATUS :** `{sudou}`\n"
        Electro_caption += f"**※┄┄➳ DEVELOPER STATUS : ACTIVE** \n"
        Electro_caption += f"**※┄┄➳ CREATOR :** ** [🇮🇳•TEAM-ELECTRO•🇮🇳](https://t.me/electro_updates)**\n"
        Electro_caption += f"**╰────────☆═━┈┈┈━═☆───────╯**\n"
        Electro_caption += "[✨𝚁𝙴𝙿𝙾✨](https://github.com/TEAM-ELECTRO/Electro) 🔹 [📜𝙻𝙸𝙲𝙴𝙽𝚂𝙴📜](https://github.com/TEAM-ELECTRO/Electro/blob/master/LICENSE)"

        await alive.client.send_file(
            alive.chat_id, Electro_IMG, caption=Electro_caption, reply_to=reply_to_id
        )
    else:
        await edit_or_reply(
            alive,
            f"**{CUSTOM_ALIVE_TEXT}**\n\n"
            f"     __**╚»★BOT INFO★«╝**__\n"
            f"**╭────────☆═━┈┈┈━═☆───────╮**\n"
            f"**※┄┄➳ BOT STATUS : WORKING NORMALLY **\n"
            f"**※┄┄➳ YOUR BOT VERSION :**`{Electroversion}`\n"
            f"**※┄┄➳ SECURITY STATUS : NO BUGS AND ERRORS **\n"
            f"**※┄┄➳ TELETHON VERSION : ** `{version.__version__}`\n"
            f"**※┄┄➳ UPTIME :** `{uptime}`\n"
            f"**※┄┄➳ SUDO STATUS :** `{sudou}`\n"
            f"**※┄┄➳ DEVELOPER STATUS : ACTIVE** \n"
            f"**※┄┄➳ CREATOR :** [🇮🇳• TEAM-ELECTRO •🇮🇳](https://t.me/ELECTRO_UPDATES)**\n"
            f"**※┄┄➳ MASTER:** {mention}\n"
            f"**╰────────☆═━┈┈┈━═☆───────╯**\n"
            "[✨REPO✨](https://github.com/TEAM-ELECTRO/Electro) 🔹 [📜LICENSE📜](https://github.com/TEAM-ELECTRO/Electro/blob/master/LICENSE)",
        )
CmdHelp("alive").add_command(
  'alive', None, 'Check weather the bot is alive or not'
  ).add_info(
  'Zinda Hai Kya Bro?'
).add()
