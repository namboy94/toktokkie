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

import os
import logging
from typing import TYPE_CHECKING
from puffotter.os import get_ext
if TYPE_CHECKING:  # pragma: no cover
    from toktokkie.metadata.music.components.MusicAlbum import MusicAlbum


class MusicVideo:
    """
    Class that keeps track of information for music videos
    """

    def __init__(self, path: str, album: "MusicAlbum"):
        """
        Initializes the music video
        :param path: The path to the video file
        :param album: The album to which the music video belongs to
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.album = album
        self.path = path
        self.format = get_ext(self.path)

    @property
    def title(self) -> str:
        """
        :return: The title of the song
        """
        return os.path.basename(self.path)\
            .rsplit(f".{self.format}", 1)[0]\
            .rsplit("-video")[0]
