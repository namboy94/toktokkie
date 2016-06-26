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
from typing import Dict, Tuple


def update(config: Dict[str, Dict[str, str]]) -> None:
    """

    :param config: show directory: (season, quality, horriblesubs-name)
    :return:
    """
    for show in config:

        meta = os.path.join(show, ".icons")  # TODO Change to .meta
        season = os.path.join(show, config[show]["season"])
        showname = os.path.basename(os.path.basename(meta))

        if not os.path.isdir(meta):
            os.makedirs(meta)
        if not os.path.isdir(season):
            os.makedirs(season)

        current_episode = len(os.listdir(season))
        while check_for_next(current_episode, config[show]["horriblesubs-name"]):
            download(current_episode, config[show]["horriblesubs-name"], showname, season)

def check_for_next() -> bool:
    pass

def download() -> None:
    pass