# Electro - UserBot
# Copyright (C) 2021 TeamElectro
# This file is a part of < https://github.com/TeamElectro/Electro/ >
# PLease read the GNU Affero General Public License in <https://www.github.com/TeamElectro/Electro/blob/main/LICENSE/>.

FROM theteamElectro/Electro:main

# set timezone
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# clone the repo and change workdir
RUN git clone https://github.com/TeamElectro/Electro.git /root/TeamElectro/
WORKDIR /root/TeamElectro/

# install main requirements.
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 uninstall av -y && pip3 install av --no-binary av

# start the bot
CMD ["bash", "resources/startup/startup.sh"]
