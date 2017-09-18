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
from typing import Dict, List
from toktokkie.utils.metadata.media_types.Base import Base


class TvSeries(Base):
    """
    Models the tv_series media type
    """

    identifier = "tv_series"
    """
    An identifier string that indicates the type
    """

    def __init__(self, path: str, generate: bool = False, overwrite_with_generated: bool = False):
        """
        Initializes the Media Type object
        :param path: The path to the media directory
        :param generate: Can be set to True to generate the directory and a basic info.json file.
        :param overwrite_with_generated: Can be set to True to overwrite any existing info.json file while generating.
        """
        super().__init__(path, generate, overwrite_with_generated)
        self.resolutions = self.info["resolutions"]
        self.audio_langs = self.info["audio_langs"]
        self.subtitle_langs = self.info["subtitle_langs"]
        self.tvdb_url = None if "tvdb_url" not in self.info else self.info["tvdb_url"]
        self.seasons = None if "seasons" not in self.info else self.info["seasons"]

    def write_changes(self):
        """
        Writes the changes in JSON data to the JSON info file
        :return: None
        """
        self.info["resolutions"] = self.resolutions
        self.info["audio_langs"] = self.audio_langs
        self.info["subtitle_langs"] = self.subtitle_langs
        self.add_noneable_to_info("tvdb_url", self.tvdb_url)
        self.add_noneable_to_info("seasons", self.seasons)
        super().write_changes()

    def get_child_names(self) -> List[str]:
        """
        Method that fetches all children items (like Seasons, for example)
        :return: A list of children names
        """
        children = os.listdir(self.path)
        children = list(filter(
            lambda x: not x.startswith(".") or not os.path.isdir(os.path.join(self.path, x)),
            children
        ))
        return children

    # noinspection PyDefaultArgument
    @staticmethod
    def define_attributes(additional: List[Dict[str, Dict[str, type]]]=[]) -> Dict[str, Dict[str, type]]:
        """
        Defines additional attributes for this media type
        :param additional: Further additional parameters for use with child classes
        :return: The attributes of the Media Type
        """
        additional.append({
            "required": {"resolutions": list, "audio_langs": list, "subtitle_langs": list},
            "optional": {"tvdb_url": str},
            "extenders": {"seasons": dict}
        })
        return super(TvSeries, TvSeries).define_attributes(additional)
