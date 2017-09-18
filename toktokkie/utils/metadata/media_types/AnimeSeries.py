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
