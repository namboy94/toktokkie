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

from typing import Dict


class MediaTypes(object):
    """
    Class containing various variables and methods to handle Media Types
    """

    """
    The Media type definitions. Always check to avoid cyclical dependencies!
    """
    types = {

        "media": {
            "attrs": {"type": ""}
        },

        "tv_series": {
            "attrs": {},  # {"seasons": {}},
            "parent": "media"
        },

        "anime_series": {
            "attrs": {},
            "parent": "tv_series"
        },

        "ebook": {
            "attrs": {"ISBN-13": "", "author": ""},
            "parent": "media"
        },

        "light_novel": {
            "attrs": {"myanimelist": "", "novelupdates": "", "licensed_status": ""},
            "parent": "ebook"
        },

        "music": {
            "attrs": {"titles": {}, "albums": {}},
            "parent": "media"
        },

        "anime_music": {
            "attrs": {},
            "parent": "music"
        }
    }

    @staticmethod
    def is_subtype_of(media_type: str, target: str) -> bool:
        """
        Checks if a media type is a subtype of another media type

        :param media_type: The media type to check
        :param target: The target type to check against
        :return: True if the type is a subtype, else False
        """

        if media_type == target:
            return True

        try:
            parent = MediaTypes.types[media_type]["parent"]
            # noinspection PyTypeChecker
            return MediaTypes.is_subtype_of(parent, target)

        except KeyError:
            return False

    # noinspection PyDefaultArgument
    @staticmethod
    def generate_basic_info_data(media_type: str, existing_data: Dict[str, object] = None) -> Dict[str, object]:
        """
        Generates a dictionary containing the contents of a barebones
        info.json file for the specified media type

        :param media_type: The media type to generate this for
        :param existing_data: Existing data. Should not generally be used externally, but rather just for recursion
        :return: The data
        """

        if existing_data is None:
            existing_data = {}

        if "type" not in existing_data:
            existing_data["type"] = media_type

        try:
            type_structure = MediaTypes.types[media_type]

            for attr in type_structure["attrs"]:
                if attr not in existing_data:
                    existing_data[attr] = type_structure["attrs"][attr]

            if media_type == "media":
                return existing_data
            else:
                parent = type_structure["parent"]
                # noinspection PyTypeChecker
                return MediaTypes.generate_basic_info_data(parent, existing_data)

        except KeyError:
            return existing_data
