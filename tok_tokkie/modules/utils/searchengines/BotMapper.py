"""
LICENSE:

Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.

LICENSE
"""

# imports
from typing import Tuple


class BotMapper(object):
    """
    Class that offers methods to map an XDCC bot to an IRC server and/or IRC channel
    """

    mapping = {"HelloKitty": ("irc.rizon.net", "#horriblesubs"),
               "CR-*": ("irc.rizon.net", "#horriblesubs"),
               "E-D|*": ("irc.rizon.net", "#exiled-destiny"),
               "Doki|*": ("irc.rizon.net", "#doki"),
               "default": ("irc.rizon.net", "#intel")}

    @staticmethod
    def get_server(xdcc_bot: str) -> str:
        """
        Determines the IRC Server for the bot

        :param xdcc_bot: the bot for which the server is wanted
        :return: the server for the specified bot
        """
        return BotMapper.get_match(xdcc_bot)[0]

    @staticmethod
    def get_channel(xdcc_bot: str) -> str:
        """
        Determines the IRC channel for the bot

        :param xdcc_bot: the bot for which the channel is wanted
        :return: the channel for the specified bot
        """
        return BotMapper.get_match(xdcc_bot)[1]

    @staticmethod
    def get_match(botname: str) -> Tuple[str, str]:
        """
        Matches a botname with a server and channel

        :param botname: the bot to check
        :return: a tuple of the server, the channel
        """
        for bot in BotMapper.mapping:
            if bot.endswith("*"):
                if botname.startswith(bot.rsplit("*", 1)[0]):
                    return BotMapper.mapping[bot]
            elif bot.startswith("*"):
                if botname.endswith(bot.split("*", 1)[1]):
                    return BotMapper.mapping[bot]
            elif bot == botname:
                return BotMapper.mapping[bot]
        return BotMapper.mapping["default"]