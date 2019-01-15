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

        volumes = []
        for volume_name in os.listdir(directory_path):

            volume_path = os.path.join(directory_path, volume_name)
            if volume_name.startswith(".") or not os.path.exists(volume_path):
                continue

            print("{}:".format(volume_name))
            ids = cls.prompt_for_ids(series_ids)

            # Remove double entries
            for id_type, id_value in series_ids.items():
                if id_value == ids.get(id_type, None):
                    ids.pop(id_type)

            volumes.append(BookVolume(series, {
                "ids": ids,
                "name": volume_name
            }))

        series.seasons = volumes
        return series

    @property
    @json_parameter
    def volumes(self) -> List[BookVolume]:
        """
        :return: A list of book volumes for this book series
        """
        return list(map(
            lambda x: BookVolume(self.directory_path, x),
            self.json["volumes"]
        ))

    @volumes.setter
    def volumes(self, seasons: List[BookVolume]):
        """
        Setter method for the volumes
        :param seasons: The volumes to set
        :return: None
        """
        self.json["volumes"] = []
        for season in seasons:
            self.json["volumes"].append(season.json)
