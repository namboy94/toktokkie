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

# /msg CR-HOLLAND|NEW xdcc send #5024
# [HorribleSubs] Flying Witch - 04 [480p].mkv
# [SUBGROUP] SHOWNAME - EPISODE [QUALITY].mkv

# imports
import os
import sys
from typing import Dict, Tuple
from tok_tokkie.scripts.single_xdcc import main as xdcc_dl
from tok_tokkie.modules.utils.searchengines.HorribleSubsGetter import HorribleSubsGetter


def update(config: Dict[str, Dict[str, str]]) -> None:
    """

    :param config: show directory: (season, quality, horriblesubs-name, bot)
    :return:
    """
    for show in config:

        meta = os.path.join(show, ".icons")  # TODO Change to .meta
        season = os.path.join(show, "Season " + config[show]["season"])
        showname = os.path.basename(os.path.basename(meta))

        if not os.path.isdir(meta):
            os.makedirs(meta)
        if not os.path.isdir(season):
            os.makedirs(season)

        while True:
            current_episode = len(os.listdir(season)) + 1
            current_episode = str(current_episode) if current_episode >= 10 else "0" + str(current_episode)
            nextcheck = check_for_next(current_episode, config[show]["horriblesubs-name"], config[show]["quality"], config[show]["bot"])
            if not nextcheck:
                break
            else:
                download(current_episode, config[show]["horriblesubs-name"], config[show]["bot"], season, str(nextcheck[1]))


def check_for_next(episode: str, horriblesubs_name: str, quality: str, bot: str) -> Tuple[bool, str] or bool:
    searcher = HorribleSubsGetter(horriblesubs_name + " " + episode + " " + quality)
    results = searcher.search()
    wanted_episode = horriblesubs_name + " - " + episode + " [" + quality + "].mkv"
    for result in results:
        if result.bot == bot and result.filename.split("] ", 1)[1] == wanted_episode:
            return True, result.packnumber
    return False


def download(episode: str, horriblesubs_name: str, bot: str, target_directory: str, packnumber: str) -> None:

    packstring = "/msg " + bot + " xdcc send #" + packnumber
    while len(sys.argv) > 1:
        sys.argv.pop()
    sys.argv.append(packstring)
    sys.argv.append(target_directory)
    xdcc_dl()