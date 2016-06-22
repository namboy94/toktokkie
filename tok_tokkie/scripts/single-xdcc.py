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

# /msg [MW]-XDCC-MOV003 xdcc send #30


# imports
import os
import sys
from typing import Tuple, List

def parse_xdcc_string(xdcc_string: str) -> Tuple[str, str]:
    """

    :param xdcc_string:
    :return:
    """

def download_pack(xdcc_bot: str, xdcc_pack: str, target: str) -> None:
    """

    :param xdcc_bot:
    :param xdcc_pack:
    :param target:
    :return:
    """

def main() -> None:
    """

    Usage: single-xdcc /msg botname xdcc send #pack destination

    :return:
    """
    bot, pack, destination = ("", "", os.getcwd())
    if len(sys.argv) == 7 and sys.argv[1] == "/msg":
        bot = sys.argv[2]
        pack = sys.argv[5].split("#")[1]
    elif len(sys.argv) == 2
