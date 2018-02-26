"""
Copyright 2015-2018 Hermann Krumrey <hermann@krumreyh.com>

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
"""

import os
import json
from toktokkie.metadata import prompt_user
from toktokkie.metadata.types.CommaList import CommaList
from toktokkie.metadata.exceptions import InvalidMetadataException


class Base:
    """
    The Base Metadata class. It defines general metadata methods and
    common interfaces.
    """

    type = "base"
    """
    The type of the Metadata. Shoudl generally be overridden by child classes
    """

    @classmethod
    def from_json(cls, json_file: str):
        """
        Generates a Metadata object from a JSON file path
        :param json_file: The path to the JSON file
        :return: The generated metadata object
        """
        with open(json_file, "r") as f:
            data = json.load(f)
        return cls(data)

    @classmethod
    def generate_from_prompts(cls, directory: str, extra_data: dict = None):
        """
        Generates a Metadata object based on user prompts
        This can and should be extended by child classes
        :param directory: The path to the directory for which to generate
                          the metadata
        :param extra_data: Additional data. to insert into the data dictionary.
                           May be used to make extending the method easier
        :return: The generated metadata object
        """
        name = os.path.basename(directory)
        print("Generating " + cls.type + " metadata for " + name)
        data = {
            "type": cls.type,
            "name": prompt_user("name", str, name),
            "tags": prompt_user("tags", CommaList, CommaList("")).list
        }

        if data is not None:
            for key, value in extra_data.items():
                data[key] = value

        return cls(data)

    def to_dict(self) -> dict:
        """
        Generates a JSON-compatible dictionary representation of the
        metadata object. Should be extended by child classes
        :return: The dictionary representation
        """
        return {
            "type": self.type,
            "name": self.type,
            "tags": self.tags
        }

    def __init__(self, json_data: dict):
        """
        Initializes the Metadata object. If the provided JSON data is incorrect
        (i.e. missing elements or invalid types), an InvalidMetadata exception
        will be thrown.
        :param json_data: The JSON dictionary to use
                          to generate the metadata object
        """
        try :
            self.name = json_data["name"]
            self.tags = json_data["tags"]
        except KeyError:
            raise InvalidMetadataException()

    def write(self, json_file: str):
        """
        Writes the metadata to a file in JSON format
        :param json_file: The path to the JSON file in
                          which to write the metadata
        :return: None
        """
        with open(json_file, "w") as f:
            f.write(json.dumps(
                self.to_dict(),
                sort_keys=True,
                indent=4,
                separators=(",", ": ")
            ))
