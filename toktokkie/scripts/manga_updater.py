"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from typing import List, Dict
from toktokkie.modules.objects.manga.MangaSeries import MangaSeries


def start(config: List[Dict[str, str]], repair: bool = False, verbose: bool = False, dry_run: bool = False,
          zip_chapters: bool = False, zip_volumes: bool = False) -> None:
    """
    Starts the manga updating process

    :param config:
    :param repair:
    :param verbose:
    :param dry_run:
    :param zip_chapters:
    :param zip_volumes:
    :return:
    """
    manga_series = []

    for manga in config:
        target_directory = manga["target_directory"]
        url = manga["manga_url"]

        manga_serie = MangaSeries(url, target_directory)
        manga_serie.set_verbose(verbose)
        manga_serie.set_dry_run(dry_run)
        manga_series.append(manga_serie)
        manga_serie.download_manga()

    for manga in manga_series:
        manga.download_manga(update=not repair, repair=repair)
        manga.zip(zip_chapters=zip_chapters, zip_volumes=zip_volumes)
