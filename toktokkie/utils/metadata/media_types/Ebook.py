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

    # Getters
    @property
    def author(self) -> str:
        return str(self.resolve_inner_attribute("author"))

    @property
    def isbn(self) -> str:  # ISBN-13
        return str(self.resolve_inner_attribute("isbn"))

    # Setters
    @author.setter
    def author(self, value: str):
        self.store_inner_attribute("author", value)

    @isbn.setter
    def isbn(self, value: str):
        self.store_inner_attribute("isbn", value)

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
