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
import json
import logging
from typing import Dict, Any, List, Optional
from jsonschema import validate, ValidationError
from toktokkie.metadata.base.Metadata import Metadata
from toktokkie.metadata.enums import MediaType
from toktokkie.exceptions import InvalidUpdateInstructions, \
    MissingUpdateInstructions


class Updater:
    """
    Class that defines the common behaviour of Updaters
    """

    def __init__(self, metadata: Metadata, args: Dict[str, Any]):
        """
        Initializes the Updater object
        :param metadata: The metadata belonging to the media to update
        :param args: The command line arguments used to configure the Updater
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.metadata = metadata
        self.args = args

        update_file = self.update_file(metadata.directory_path)
        self.config = {}  # type: Dict[str, Any]

        if self.json_schema() is not None:
            if os.path.isfile(update_file):
                with open(update_file, "r") as f:
                    self.config = json.load(f)
            else:
                raise MissingUpdateInstructions(self.update_file)

        self.validate()

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the Updater
        """
        raise NotImplementedError()

    @classmethod
    def update_file(cls, meta_dir: str) -> str:
        """
        Generates the path to the update file
        :param meta_dir: The meta directory
        :return:
        """
        return os.path.join(
            meta_dir,
            ".meta/{}_update.json".format(cls.name())
        )

    @classmethod
    def applicable_media_types(cls) -> List[MediaType]:
        """
        :return: A list of media type with which the updater can be used with
        """
        raise NotImplementedError()

    @classmethod
    def json_schema(cls) -> Optional[Dict[str, Any]]:
        """
        :return: Optional JSON schema for a configuration file
        """
        return None

    @classmethod
    def prompt(cls, metadata: Metadata):
        """
        Prompts the user for information to create a config file
        :param metadata: The metadata of the media for which to create an
                         updater config file
        :return: None
        """
        config = cls._prompt(metadata)
        if config is not None:
            with open(cls.update_file(metadata.directory_path), "w") as f:
                json.dump(config, f, indent=4)

    # noinspection PyUnusedLocal
    @classmethod
    def _prompt(cls, metadata: Metadata) -> Optional[Dict[str, Any]]:
        """
        Prompts the user for information to create a config file
        This method is meant to be overridden by subclasses
        :param metadata: The metadata of the media for which to create an
                         updater config file
        :return: The configuration JSON data
        """
        logging.getLogger(__name__).warning(
            "This Updater does not support update config files"
        )
        return None

    def update(self):
        """
        Executes the update
        :return: None
        """
        raise NotImplementedError()

    def validate(self):
        """
        Checks if the configuration is valid
        :return: None
        """
        if self.json_schema() is not None:
            try:
                validate(instance=self.config, schema=self.json_schema())
            except ValidationError as e:
                raise InvalidUpdateInstructions(str(e))
