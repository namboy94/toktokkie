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

import json
from abc import ABC
from typing import Optional, Dict, Any
from toktokkie.neometadata.base.Renamer import Renamer
from toktokkie.neometadata.base.Validator import Validator
from toktokkie.neometadata.base.Prompter import Prompter


class Metadata(Renamer, Validator, Prompter, ABC):
    """
    Class that combines the various Metadata classes and defines a constructor
    """

    def __init__(
            self,
            directory_path: str,
            json_data: Optional[Dict[str, Any]] = None,
            no_validation: bool = False
    ):
        """
        Inititalizes the metadata object using JSON data
        :param directory_path: The directory of the media for which to
                               generate the metadata
        :param json_data: Optional metadata JSON.
                          Will be used instead of info.json metadata
                          if provided
        :param no_validation: Skips JSON validation if True
        :raises InvalidMetadataException: if the metadata could not be
                                          parsed correctly
        """
        self.directory_path = directory_path

        if json_data is None:
            with open(self.metadata_file, "r") as info:
                self.json = json.load(info)
        else:
            self.json = json_data

        if not no_validation:
            self.validate()

    def __repr__(self) -> str:
        """
        :return: A string that could re-generate the metadata object
        """
        return "{}({}, {})".format(
            self.__class__.__name__,
            self.directory_path,
            str(self.json)
        )
