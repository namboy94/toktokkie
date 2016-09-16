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
import os
from toktokkie.modules.utils.manga.MangaScraperManager import MangaScraperManager


class MangaSeries(object):
    """
    Class that models a Manga series. It is the entry point for all operations
    related to downloading, repairing and zipping manga series.

    It offers an automatic scraper detection system that tries to find a fitting scraper for
    the URL provided
    """

    url = ""
    """
    The manga series' URL
    """

    name = ""
    """
    The manga series' name
    """

    root_directory = ""
    """
    The root directory of the downloaded manga
    """

    scraper = None
    """
    The scraper used to find the volumes belonging to the series
    """

    volumes = []
    """
    List of volumes of the series
    """

    verbose = False
    """
    Flag that can be set to enable console output
    """

    dry_run = False
    """
    Flag that can be set to disable any changes to the system, i.e. a dry run akin
    to the rsync dry run flag '-n'
    """

    def __init__(self, url: str, name: str, root_directory: str) -> None:
        """
        Initializes the Manga series

        :param url: the URL for where to look for volumes to download
        :param name: the name of the series
        :param root_directory: the directory in which the local copy of the series resides in
        """

        self.url = url
        self.name = name
        self.root_directory = root_directory
        self.scraper = MangaScraperManager.get_scraper_for(url)  # Automatically find the correct scraper

    def scrape(self) -> None:
        """
        Finds a list of all volumes using the scraper found in the __init__ method
        :return:
        """
        self.volumes = self.scraper.scrape_volumes_from_url(self.url)

    def update(self) -> None:
        """
        Updates the current directory with volumes and chapters that do not exist yet

        :return: None
        """
        for volume in self.volumes:
            pass

    def repair(self) -> None:
        """
        Updates the current directory with volumes and chapters that do not exist yet
        While doing so, every file is checked for consistency and repaced if needed

        :return: None
        """
        for volume in self.volumes:
            pass

    def zip_chapters(self) -> None:
        """
        Zips the series by chapter

        :return: None
        """
        for volume in os.listdir(self.root_directory):
            pass

    def zip_volumes(self) -> None:
        """
        Zips the series by volume

        :return: None
        """
        for volume in os.listdir(self.root_directory):
            pass

    def zip_all(self) -> None:
        """
        Zips the series by Volume and then by chapter

        :return: None
        """
        self.zip_volumes()
        self.zip_chapters()

    def set_verbose(self, verbose: bool = True) -> None:
        """
        Sets the verbosity flag

        :param verbose: the new value of the verbosity flag, defaults to True
        :return: None
        """
        self.verbose = verbose

    def set_dry_run(self, dry_run: bool = True) -> None:
        """
        Sets the dry_run flag

        :param dry_run: the new value of the dry_run flag, defaults to True
        :return: None
        """
        self.dry_run = dry_run
