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
from toktokkie.enums import IdType, MediaType
from toktokkie.metadata.base.Metadata import Metadata
from toktokkie.metadata.music.MusicPrompter import MusicPrompter
from toktokkie.metadata.music.MusicRenamer import MusicRenamer
from toktokkie.metadata.music.MusicValidator import MusicValidator


class Music(Metadata, MusicRenamer, MusicPrompter, MusicValidator):
    """
    Metadata class that handles music/artists
    """

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The MusicArtist media type
        """
        return MediaType.MUSIC_ARTIST

    @classmethod
    def valid_id_types(cls) -> List[IdType]:
        """
        :return: A list of valid ID types
        """
        return [
            IdType.MUSICBRAINZ_ARTIST
        ]
