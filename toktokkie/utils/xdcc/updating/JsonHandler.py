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

# imports
import json
from toktokkie.utils.xdcc.updating.objects.Series import Series


class JsonHandler(object):
    """
    Class that handles storing and loading JSON configs for the XDCC Updater
    """

    def __init__(self, json_file: str = None) -> None:
        """
        Creates a new JsonHandler, either from scratch or from an exisitng JSON file

        :param json_file: An optional JSON file location.
        """
        self.json_data = []

        if json_file is not None:
            self.json_data = json.load(json_file)

    def store_json(self, destination: str) -> None:
        """
        Stores the current JSON data in a JSON file

        :param destination: The destination JSON file
        :return:            None
        """
        with open(destination, 'w') as f:
            json.dump(self.json_data, f)

    def add_series(self, series: Series) -> None:
        """
        Adds a Series to the JSON Data

        :param series:
        :return:
        """
        self.json_data.append(series.to_dict())

    def remove_series(self, series: Series) -> None:
        """
        Removes a series from the JSON Data

        :param series: The series to remove
        :return:       None
        """
        pop_index = None
        for i, show in enumerate(self.json_data):
            if series.is_same(show):
                pop_index = i

        if pop_index is not None:
            self.json_data.pop(pop_index)
