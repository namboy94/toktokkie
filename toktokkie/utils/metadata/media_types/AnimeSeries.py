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

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from toktokkie.utils.metadata.media_types.TvSeries import TvSeries


class AnimeSeries(TvSeries):
    """
    Models the anime_series media type
    """

    identifier = "anime_series"
    """
    An identifier string that indicates the type
    """

    @property
    def myanimelist_url(self) -> str:
        url = self.resolve_inner_attribute("myanimelist_url")
        return url if url is not None else ""

    @myanimelist_url.setter
    def myanimelist_url(self, value: str):
        url = None if value == "" else value
        self.store_inner_attribute("myanimelist_url", url)

    def load_myanimelist_data(self) -> Dict[str, str or int or List[str]]:
        """
        Fetches information from myanimelist.net for this metadata object
        :return: A dictionary with information from myanimelist.net with chosen default values in
                 case any values were not found
        """

        data = {
            "type": "?",
            "episodes": -1,
            "status": "?",
            "aired": "?",
            "studios": [],
            "source": "?",
            "genres": [],
            "runtime": "?",
            "score": "?",
            "rank": "?"
        }

        html = requests.get(self.myanimelist_url)
        retries = 0
        while html.status_code != 200 and retries < 10:
            time.sleep(1)
            retries += 1
            html = requests.get(self.myanimelist_url)

        soup = BeautifulSoup("" if html.status_code != 200 else html.text, "html.parser")
        sidebar = soup.find_all("div", "js-scrollfix-bottom")

        if len(sidebar) == 0:
            return data

        divs = sidebar[0].find_all("div")

        for div in divs:
            text = div.text.replace("\n", "").strip()

            if text.startswith("Type:"):
                data["type"] = text.split(":")[1].strip()
            elif text.startswith("Episodes:"):
                data["episodes"] = int(text.split(":", 1)[1].strip())
            elif text.startswith("Status:"):
                data["status"] = text.split(":", 1)[1].strip()
            elif text.startswith("Aired:"):
                data["aired"] = text.split(":", 1)[1].strip()
            elif text.startswith("Studios:"):
                data["studios"] = text.split(":", 1)[1].strip().split(",")
            elif text.startswith("Source:"):
                data["source"] = text.split(":", 1)[1].strip()
            elif text.startswith("Genres:"):
                data["genres"] = text.split(":", 1)[1].strip().split(",")
            elif text.startswith("Duration:"):
                data["runtime"] = text.split(":", 1)[1].strip()
            elif text.startswith("Score:"):
                data["score"] = text.split(":", 1)[1].split("(")[0].strip()
            elif text.startswith("Ranked:"):
                data["rank"] = text.split(":", 1)[1].strip().split(" ")[0].strip()

        return data

    # noinspection PyDefaultArgument
    @staticmethod
    def define_attributes(additional: List[Dict[str, Dict[str, type]]]=[]) -> Dict[str, Dict[str, type]]:
        """
        Defines additional attributes for this media type
        :param additional: Further additional parameters for use with child classes
        :return: The attributes of the Media Type
        """
        additional.append({
            "required": {},
            "optional": {"myanimelist_url": str},
            "extenders": {}
        })
        return super(AnimeSeries, AnimeSeries).define_attributes(additional)
