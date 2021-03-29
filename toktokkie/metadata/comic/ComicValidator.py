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

from abc import ABC
from typing import Dict, Any
from toktokkie.metadata.base.Validator import Validator
from toktokkie.metadata.comic.ComicExtras import ComicExtras


class ComicValidator(Validator, ComicExtras, ABC):
    """
    Implements the Validator functionality for comic metadata
    """

    @classmethod
    def build_schema(cls) -> Dict[str, Any]:
        """
        Generates the JSON schema
        :return: The JSON schema
        """
        base = super().build_schema()
        base["properties"].update({
            "special_chapters": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "chapter_offset": {
                "type": "integer"
            }
        })
        return base
