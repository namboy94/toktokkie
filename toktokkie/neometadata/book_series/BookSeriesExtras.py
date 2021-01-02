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
from typing import Dict
from puffotter.os import listdir
from toktokkie.neometadata.book_series.components.BookVolume import BookVolume
from toktokkie.neometadata.base.MetadataBase import MetadataBase


class BookSeriesExtras(MetadataBase, ABC):
    """
    Additional methods and attributes for book series metadata objects
    """

    @property
    def volumes(self) -> Dict[int, BookVolume]:
        """
        :return: A list of book volumes for this book series
        """
        volumes = {}  # type: Dict[int, BookVolume]
        volume_files = listdir(self.directory_path, no_dirs=True)

        for i, (_, volume_path) in enumerate(volume_files):
            volume_num = i + 1
            json_data = self.json["volumes"].get(str(volume_num), {"ids": {}})
            volumes[i + 1] = BookVolume(
                volume_num, volume_path, self.ids, json_data
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
