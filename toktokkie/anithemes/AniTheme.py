"""LICENSE
Copyright 2015 Hermann Krumrey <hermann@krumreyh.com>

This file is part of toktokkie.

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
LICENSE"""

import os
import json
import time
import logging
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple, Dict, Any
from puffotter.subprocess import execute_command
from puffotter.requests import aggressive_request
from puffotter.os import replace_illegal_ntfs_chars
from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.models.attributes.MediaType import MediaType


class AniTheme:
    """
    Class that contains all relevant information for an anime theme song.
    Uses reddit and myanimelist to retrieve all the information
    # TODO Integrate AniDB, since it has way more info on artists etc
    """

    mal_cache = {}  # type: Dict[int, Dict[str, Any]]
    """
    Cache for repeated myanimelist requests
    """

    logger = logging.getLogger(__name__)
    """
    Logger for this class
    """

    def __init__(
            self,
            show_name: str,
            mal_id: int,
            theme_type: str,
            song_name: str,
            episodes: str,
            media_url: str
    ):
        """
        Initializes the anime theme. Loads missing data from the internet
        while initializing, so this might take up to a couple of seconds.
        :param show_name: The name of the show this songe is a theme song for
        :param mal_id: The myanimelist ID of that show
        :param theme_type: The type of theme (example: OP, ED)
        :param song_name: The name of the song
        :param episodes: During which episodes the theme song played
        :param media_url: The URL to the video of this theme song
        """
        self.logger.info("Initializing {}".format(song_name))

        self.show_name = replace_illegal_ntfs_chars(show_name)
        self.mal_id = mal_id
        self.anilist_id = AnilistApi().get_anilist_id_from_mal_id(
            MediaType.ANIME, self.mal_id
        )
        self._theme_type = theme_type
        if "OP" in theme_type:
            self.theme_type = "OP"
        elif "ED" in theme_type:
            self.theme_type = "ED"
        else:
            self.theme_type = "Unknown"

        self.alternate_version = False
        if "v" in self._theme_type.lower():
            self.alternate_version = "v1" not in self._theme_type.lower()

        self.song_name = replace_illegal_ntfs_chars(song_name)
        self.episodes = episodes
        self.media_url = media_url

        self.filename = "{} {} - {}".format(
            self.show_name, theme_type, self.song_name
        )

        self.temp_webm_file = os.path.join("/tmp", self.filename + ".webm")
        self.temp_mp3_file = os.path.join("/tmp", self.filename + ".mp3")
        self.temp_cover_file = os.path.join("/tmp", self.filename + ".png")

        self.mal_title, self.artist = self.__load_song_info()
        self.mal_title = replace_illegal_ntfs_chars(self.mal_title)
        self.artist = replace_illegal_ntfs_chars(self.artist)

        if song_name.lower() not in self.mal_title.lower():
            self.logger.warning("Song title mismatch: [{}!={}]".format(
                song_name, self.mal_title
            ))
        if self.artist == "Unknown" or self.artist.strip() == "":
            self.logger.warning("Unknown artist")

        self.logger.info(self)

    def __str__(self) -> str:
        """
        :return: A string representation of the object
        """
        return "{} {}, Title: \"{}\", Artist: \"{}\", Eps: \"{}\"".format(
            self.show_name,
            self._theme_type,
            self.song_name,
            self.artist,
            self.episodes
        )

    @classmethod
    def load_reddit_anithemes_wiki_info(
            cls,
            year: int,
            season: str,
            whitelist: Optional[List[str]] = None
    ) -> List["AniTheme"]:
        """
        Loads all theme songs for a specific season and year
        CAUTION: Currently season does nothing, it is recommended to use
        the whitelist parameter to limit the requests done
        :param year: The year for which to fetch the theme songs
        :param season: The season for which to fetch the theme songs
        :param whitelist: If provided, will ignore any series that are not
                          contained in the whitelist
        :return: The fetched AniTheme objects
        """

        cls.logger.info("Loading theme info for {} {}".format(season, year))

        url = "https://old.reddit.com/r/AnimeThemes/wiki/" \
              "{}#wiki_{}_{}_season".format(year, year, season)
        response = aggressive_request(url)

        soup = BeautifulSoup(response, "html.parser")
        listings = soup.find("div", {"class": "md wiki"})

        children = list(listings.children)

        while children[0].name != "h3":
            children.pop(0)

        current_title = ""
        current_mal_id = 0
        current_tables = []  # type: List[BeautifulSoup]
        themes = []  # type: List[AniTheme]
        while len(children) > 0:
            element = children.pop(0)

            if element.name == "h3":
                if current_title != "" \
                        and (whitelist is None or current_title in whitelist):
                    print("Loading themes for {}".format(current_title))

                    data = []  # type: List[AniTheme]
                    while len(current_tables) > 0:
                        data += cls.__parse_reddit_wiki_table(
                            current_title,
                            current_mal_id,
                            current_tables.pop(0)
                        )
                    themes += data

                current_title = element.text
                current_tables = []
                mal_url = element.find_all("a")[0]["href"]
                if mal_url.endswith("/"):
                    mal_url = mal_url[0:-1]
                try:
                    current_mal_id = int(mal_url.rsplit("/", 1)[1])
                except ValueError:
                    current_mal_id = int(mal_url.rsplit("/", 2)[1])

            elif element.name == "table":
                current_tables.append(element)

        return themes

    @classmethod
    def __parse_reddit_wiki_table(
            cls,
            title: str,
            mal_id: int,
            table
    ) -> List["AniTheme"]:
        """
        Parses a table from reddit and generates AniTheme objects from them
        :param title: The title of the series associated with the table
        :param mal_id: The myanimelist ID of the series
        :param table: The table to parse
        :return: A list of AniTheme objects parsed from the content of
                 the table
        """
        data = []

        for row in table.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) == 0:
                continue
            description = columns[0].text

            try:
                link = columns[1].find("a")["href"]
            except TypeError:  # Avoid missing links
                continue

            if not description:
                continue

            data.append(cls(
                show_name=title,
                theme_type=description.split("\"", 1)[0].strip(),
                song_name=description.split("\"", 1)[1].rsplit("\"", 1)[0],
                media_url=link,
                mal_id=mal_id,
                episodes=columns[2].text
            ))
        return data

    def __load_song_info(self) -> Tuple[str, str]:
        """
        Loads song information using myanimelist (like artist etc)
        :return: A tuple consisting of the song title and the artist.
                 If it was not possible to figure out using myanimelist data,
                 both will be "Unknown"
        """
        self.logger.info("Loading song data using myanimelist")

        url = "https://api.jikan.moe/v3/anime/{}".format(self.mal_id)
        resp = aggressive_request(url)

        if self.mal_id is AniTheme.mal_cache:
            info = AniTheme.mal_cache[self.mal_id]
        else:
            info = json.loads(resp)
        AniTheme.mal_cache[self.mal_id] = info

        if self.theme_type == "OP":
            prefix = "opening"
        elif self.theme_type == "ED":
            prefix = "ending"
        else:
            return "Unknown", "Unknown"

        song_number = self._theme_type\
            .lower()\
            .replace("op", "")\
            .replace("ed", "")\
            .split("v")[0]\
            .strip()

        if song_number == "":
            song_number = "1"
        song_index = int(song_number) - 1

        songs = info[prefix + "_themes"]
        self.logger.debug(songs)
        self.logger.debug("Using index {} ({})"
                          .format(song_index, self._theme_type))

        try:
            song_info = songs[song_index]
            self.logger.debug(song_info)

            splitted = song_info.split("\"", 2)
            if len(splitted) == 2:
                splitted = [""] + splitted[1].replace("\"", "").split(" by ")
            title = splitted[1]
            artist = splitted[2].replace("by ", "").strip()
            return title, artist
        except IndexError:
            return "Unknown", "Unknown"

    def download_webm(self):
        """
        Downloads the .webm video of the anime theme song to the tmp directory
        :return: None
        """
        command = ["curl", "-o", self.temp_webm_file, self.media_url]

        if os.path.exists(self.temp_webm_file) \
                and os.path.getsize(self.temp_webm_file) > 1000:
            # Skip existing file
            return

        retry_count = 0
        while execute_command(command) != 0:

            if retry_count > 3:
                self.logger.warning("File download failed")
                return
            retry_count += 1

            self.logger.warning("Couldn't download theme, retrying...")
            time.sleep(15)

    def convert_to_mp3(self):
        """
        Converts the previously downloaded webm file to mp3
        :return: None
        """
        command = [
            "ffmpeg",
            "-i", self.temp_webm_file,
            "-vn",
            "-ab", "160k",
            "-ar", "44100",
            "-y", self.temp_mp3_file
        ]

        if not os.path.exists(self.temp_mp3_file):
            execute_command(command)
