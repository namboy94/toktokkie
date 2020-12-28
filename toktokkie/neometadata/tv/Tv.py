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
from toktokkie.neometadata.enums import IdType, MediaType
from toktokkie.neometadata.base.Metadata import Metadata
from toktokkie.neometadata.tv.TvRenamer import TvRenamer
from toktokkie.neometadata.tv.TvValidator import TvValidator
from toktokkie.neometadata.tv.TvPromter import TvPrompter


class Tv(Metadata, TvRenamer, TvValidator, TvPrompter):
    """
    Metadata class for TV Series
    """

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The media type of the Metadata class
        """
        return MediaType.TV_SERIES

    @classmethod
    def valid_id_types(cls) -> List[IdType]:
        """
        :return: Valid ID types for the metadata
        """
        return [
            IdType.ANILIST,
            IdType.MYANIMELIST,
            IdType.KITSU,
            IdType.IMDB,
            IdType.TVDB
        ]
