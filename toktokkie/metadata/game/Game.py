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

from typing import List
from toktokkie.metadata.base.Metadata import Metadata
from toktokkie.metadata.game.GamePrompter import GamePrompter
from toktokkie.metadata.game.GameRenamer import GameRenamer
from toktokkie.metadata.game.GameValidator import GameValidator
from toktokkie.metadata.enums import IdType, MediaType


class Game(Metadata, GameRenamer, GamePrompter, GameValidator):
    """
    Metadata class that handles games
    """

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The Game media type
        """
        return MediaType.GAME

    @classmethod
    def valid_id_types(cls) -> List[IdType]:
        """
        :return: A list of valid ID types
        """
        return [
            IdType.VNDB
        ]
