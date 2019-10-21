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
import logging
from typing import List, Optional, Dict, Any
from bs4 import BeautifulSoup
from puffotter.requests import aggressive_request
from puffotter.graphql import GraphQlClient
from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.models.attributes.MediaType import MediaType


class AniTheme:
    """
    Class that contains all relevant information for anime themes
    """

    logger = logging.getLogger(__name__)

    def __init__(
            self,
            show_name: str,
            mal_id: int,
            theme_type: str,
            song_name: str,
            media_url: str
    ):
        self.show_name = show_name
        self.mal_id = mal_id
        self.anilist_id = AnilistApi().get_anilist_id_from_mal_id(
            MediaType.ANIME, self.mal_id
        )
        self.theme_type = theme_type
        self.song_name = song_name
        self.media_url = media_url

        self.filename = "{} {} - {}".format(show_name, theme_type, song_name)
        self.temp_webm_file = os.path.join("/tmp", self.filename + ".webm")
        self.temp_mp3_file = os.path.join("/tmp", self.filename + ".mp3")
        self.temp_cover_file = os.path.join("/tmp", self.filename + ".png")

        mal_data = self.__load_mal_data()
        self.mal_openings = mal_data["openings"]
        self.mal_endings = mal_data["endings"]
        self.anilist_cover_url = self.__load_anilist_cover_url()

    @classmethod
    def load_reddit_anithemes_wiki_info(cls, year: int, season: str) \
            -> Dict[str, List["AniTheme"]]:

        url = "https://old.reddit.com/r/AnimeThemes/wiki/" \
              "{}#wiki_{}_{}_season".format(year, year, season)
        response = aggressive_request(url)

        soup = BeautifulSoup(response, "html.parser")
        listings = soup.find("div", {"class": "md wiki"})

        series_info = {}
        children = list(listings.children)

        while children[0].name != "h3":
            children.pop(0)

        current_title = ""
        current_mal_id = 0
        current_tables = []
        while len(children) > 0:
            element = children.pop(0)

            if element.name == "h3":
                if current_title != "":

                    data = []
                    while len(current_tables) > 0:
                        data += cls.__parse_reddit_wiki_table(
                            current_title,
                            current_mal_id,
                            current_tables.pop(0)
                        )
                    series_info[current_title] = data

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

        return series_info

    @classmethod
    def __parse_reddit_wiki_table(
            cls,
            title: str,
            mal_id: int,
            table
    ) -> List["AniTheme"]:
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
                mal_id=mal_id
            ))
        return data

    def __load_mal_data(self) -> Dict[str, Any]:
        """
        Loads information about the anitheme from myanimelist
        :return: The information fetched from myanimelist
        """
        url = "https://api.jikan.moe/v3/anime/{}".format(self.mal_id)
        resp = aggressive_request(url)
        info = json.loads(resp)

        song_info = {"opening_themes": [], "ending_themes": []}
        for song_type in song_info.keys():
            for song in info[song_type]:
                title = song.split("\"", 2)[1]
                artist = song.split("\"", 2)[2] \
                    .replace("by ", "") \
                    .split("(")[0] \
                    .strip()
                episodes = song.split("\"", 2)[2].split("(")
                if len(episodes) > 1:
                    episodes = episodes[1].split(")")[0].strip()
                else:
                    episodes = ""
                song_info[song_type].append((title, artist, episodes))

        return {
            "title": info["title"],
            "cover": info["image_url"],
            "openings": song_info["opening_themes"],
            "endings": song_info["ending_themes"]
        }

    def __load_anilist_cover_url(self) -> str:
        client = GraphQlClient("https://graphql.anilist.co")
        query = """
            query ($id: Int) {
                Media (id: $id) {
                    coverImage {
                        large
                    }
                }
            }
        """
        self.logger.info("Fetching cover art for {}".format(self.show_name))
        data = client.query(query, {"id": int(anilist_id[0])})["data"]
        cover_image = data["Media"]["coverImage"]["large"]
        cover_image = cover_image.replace("medium", "large")
        img = requests.get(
            cover_image, headers={"User-Agent": "Mozilla/5.0"}
        )
        if img.status_code >= 300:
            med_url = cover_image.replace("large", "medium")
            img = requests.get(
                med_url, headers={"User-Agent": "Mozilla/5.0"}
            )
        with open(tmp_file, "wb") as f:
            f.write(img.content)