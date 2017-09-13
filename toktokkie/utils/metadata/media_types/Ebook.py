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
from toktokkie.utils.metadata.media_types.Base import Base


class Ebook(Base):
    """
    Models the ebook media type
    """

    identifier = "ebook"
    """
    An identifier string that indicates the type
    """

    def __init__(self, path: str):
        """
        Initializes the Media Type object
        :param path: The path to the media directory
        """
        super().__init__(path)
        self.author = self.info["author"]
        self.isbn = self.info["isbn"] if self.info["isbn"] is not "N/A" else None

    def write_changes(self):
        """
        Writes the changes in JSON data to the JSON info file
        :return: None
        """
        self.info["author"] = self.author
        self.info["isbn"] = self.isbn if self.isbn is not None else "N/A"
        super().write_changes()

    # noinspection PyDefaultArgument
    @staticmethod
    def define_attributes(additional: List[Dict[str, Dict[str, type]]]=[]) -> Dict[str, Dict[str, type]]:
        """
        Defines additional attributes for this media type
        :param additional: Further additional parameters for use with child classes
        :return: The attributes of the Media Type
        """
        additional.append({
            "required": {"author": str, "isbn": str},
            "optional": {},
            "extenders": {}
        })
        return super(Ebook, Ebook).define_attributes(additional)
