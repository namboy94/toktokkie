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
from tok_tokkie.scripts.anime_updater import update


config = {

    "/home/hermann/Downloads/Updater/Space Patrol Luluco":
        {"horriblesubs-name": "Space Patrol Luluco", "quality": "480p", "season": "1", "bot": "CR-HOLLAND|NEW"}

}


if __name__ == '__main__':
    update(config)
