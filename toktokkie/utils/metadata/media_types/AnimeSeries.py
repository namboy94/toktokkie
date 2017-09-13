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

from typing import Dict, List
from toktokkie.utils.metadata.media_types.TvSeries import TvSeries


class AnimeSeries(TvSeries):
    """
    Models the anime_series media type
    """

    def __init__(self, path: str):
        """
        Initializes the Media Type object
        :param path: The path to the media directory
        """
        super().__init__(path)
        self.myanimelist_url = None if "myanimelist_url" not in self.info else self.info["myanimelist_url"]

    def write_changes(self):
        """
        Writes the changes in JSON data to the JSON info file
        :return: None
        """
        self.add_noneable_to_info("myanimelist_url", self.myanimelist_url)
        super().write_changes()

    # noinspection PyDefaultArgument
    @staticmethod
    def define_attributes(additional: List[Dict[str, Dict[str, type]]] = []) -> Dict[str, Dict[str, type]]:
        """
        Defines additional attributes for this media type
        :param additional: Further additional parameters for use with child classes
        :return: The attributes of the Media Type
        """
        additional.append({
            "required": {},
            "optional": {"myanimelist_url"},
            "extenders": {}
        })
        return super().define_attributes(additional)
