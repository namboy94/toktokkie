#!/usr/bin/python3
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
import os
import sys
from typing import Tuple

from tok_tokkie.modules.utils.searchengines.BotMapper import BotMapper
from tok_tokkie.modules.utils.ProgressStruct import ProgressStruct
from tok_tokkie.modules.utils.downloaders.implementations.IrcLibImplementation import IrcLibImplementation


def parse_xdcc_string(xdcc_string: str) -> Tuple[str, str]:
    """

    :param xdcc_string:
    :return:
    """
    bot = xdcc_string.split(" ")[1]
    pack = xdcc_string.split(" ")[4].split("# ")[1]
    return bot, pack


def download_pack(xdcc_bot: str, xdcc_pack: int, target_directory: str, filename_override: str) -> None:
    """

    :param xdcc_bot:
    :param xdcc_pack:
    :param target_directory:
    :param filename_override:
    :return:
    """
    bot_mapper = BotMapper(xdcc_bot)
    downloader = IrcLibImplementation(bot_mapper.server,
                                      bot_mapper.channel,
                                      xdcc_bot,
                                      xdcc_pack,
                                      target_directory,
                                      ProgressStruct(),
                                      file_name_override=filename_override)
    downloader.start()


def check_target_directory(args_maxlength: int) -> Tuple[str, str]:
    """

    :param args_maxlength:
    :return:
    """
    if len(sys.argv) == args_maxlength:
        path = sys.argv[args_maxlength - 1]
        if os.path.isdir(path):
            return path, ""
        else:
            directory = os.path.dirname(path)
            if not os.path.isdir:
                os.makedirs(directory)
            return directory, os.path.basename(path)
    else:
        return os.getcwd(), ""


def main(script_name: str) -> None:
    """

    Usage: single-xdcc /msg botname xdcc send #pack destination

    :param script_name:
    :return:
    """
    if len(sys.argv) in range(6, 7) and sys.argv[1] == "/msg":
        bot = sys.argv[2]
        pack = sys.argv[5].split("#")[1]
        destination_dir, override_filename = check_target_directory(7)
    elif len(sys.argv) in range(1, 2) and sys.argv[1].startswith("/msg"):
        bot, pack = parse_xdcc_string(sys.argv[1])
        destination_dir, override_filename = check_target_directory(2)
    else:
        print("Invalid parameters.")
        print("Usage:\n")
        print(script_name + " /msg BOTNAME xdcc send #PACKNUMBER [destination_file]")
        print(script_name + " \"/msg BOTNAME xdcc send #PACKNUMBER\" [destination_file]")
        sys.exit(1)

    download_pack(bot, int(pack), destination_dir, override_filename)
