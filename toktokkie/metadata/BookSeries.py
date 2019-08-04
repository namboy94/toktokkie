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
from typing import List
from puffotter.os import listdir
from toktokkie.metadata.Book import Book
from toktokkie.metadata.components.BookVolume import BookVolume
from toktokkie.metadata.helper.wrappers import json_parameter
from toktokkie.metadata.components.enums import MediaType


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

    @classmethod
    def prompt(cls, directory_path: str) -> Book:
        """
        Generates a new Metadata object using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata object
        """
        print("Generating metadata for {}:"
              .format(os.path.basename(directory_path)))

        series_ids = cls.prompt_for_ids()
        series = cls(directory_path, {
            "volumes": [],
            "ids": series_ids,
            "type": cls.media_type().value
        })

        volumes = {}
        for i, volume_name in enumerate(sorted(os.listdir(directory_path))):

            volume_path = os.path.join(directory_path, volume_name)
            if volume_name.startswith(".") or not os.path.exists(volume_path):
                continue

            print("Volume {} ({}):".format(i + 1, volume_name))
            ids = cls.prompt_for_ids(series_ids)

            # Remove double entries
            for id_type, id_value in series_ids.items():
                if id_value == ids.get(id_type, None):
                    ids.pop(id_type)

            if len(ids) == 0:
                continue
            else:
                volumes[i] = BookVolume(series, {
                    "ids": ids,
                    "name": volume_name
                })

        series.volumes = volumes
        return series

    @property
    @json_parameter
    def volumes(self) -> List[BookVolume]:
        """
        :return: A list of book volumes for this book series
        """
        volumes = []
        volume_files = listdir(self.directory_path, no_dirs=True)

        for i, (volume, volume_file) in enumerate(volume_files):
            json_data = self.json["volumes"].get(i, {
                "ids": self.ids,
                "name": volume
            })
            volumes.append(BookVolume(self, json_data))
        return volumes

    @volumes.setter
    def volumes(self, volumes: List[BookVolume]):
        """
        Setter method for the volumes
        :param volumes: The volumes to set
        :return: None
        """
        self.json["volumes"] = {}
        for i, volume in enumerate(volumes):
            self.json["volumes"][i] = volume.json
