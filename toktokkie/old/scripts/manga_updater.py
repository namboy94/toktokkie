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
from toktokkie.old.objects.manga.MangaSeries import MangaSeries


def start(config: List[Dict[str, str]], max_threads: int = 1, repair: bool = False, verbose: bool = False,
          dry_run: bool = False, zip_chapters: bool = False, zip_volumes: bool = False) -> None:
    """
    Starts the manga updating process

    :param config: the config in form of a list of dictionaries, as defined in the template file
    :param max_threads: maximum amount of concurrent threads
    :param repair: sets the Manga Series 'repair' flag
    :param verbose: sets the Manga Series 'verbose' flag
    :param dry_run: sets the Manga Series 'dry_run' flag
    :param zip_chapters: Zips the chapters afterwards
    :param zip_volumes: Zips the volumes afterwards
    :return: None
    """
    manga_series = []

    for manga in config:
        target_directory = manga["target_directory"]
        url = manga["manga_url"]

        manga_serie = MangaSeries(url, target_directory)
        manga_serie.set_verbose(verbose)
        manga_serie.set_dry_run(dry_run)
        manga_serie.set_maximum_thread_amount(max_threads)
        manga_series.append(manga_serie)

    for manga in manga_series:
        manga.download_manga(update=not repair, repair=repair)
        manga.zip(zip_chapters=zip_chapters, zip_volumes=zip_volumes)
