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

from typing import Dict
from puffotter.os import listdir
from toktokkie.metadata.types.Book import Book
from toktokkie.metadata.types.components.BookVolume import BookVolume
from toktokkie.metadata.MediaType import MediaType


class BookSeries(Book):
    """
    Metadata class that models a Book series
    """

    @classmethod
    def media_type(cls) -> MediaType:
        """
        :return: The media type of the Metadata class
        """
        return MediaType.BOOK_SERIES

    @property
    def volumes(self) -> Dict[int, BookVolume]:
        """
        :return: A list of book volumes for this book series
        """
        volumes = {}  # type: Dict[int, BookVolume]
        volume_files = listdir(self.directory_path, no_dirs=True)

        for i, (volume, volume_file) in enumerate(volume_files):
            volume_num = i + 1
            json_data = self.json["volumes"].get(str(volume_num), {"ids": {}})
            volumes[i + 1] = BookVolume(
                volume_num, volume, volume_file, self.ids, json_data
            )
        return volumes

    @volumes.setter
    def volumes(self, volumes: Dict[int, BookVolume]):
        """
        Setter method for the volumes
        :param volumes: The volumes to set
        :return: None
        """
        self.json["volumes"] = {}
        for i, volume in volumes.items():
            self.json["volumes"][str(i)] = volume.json
