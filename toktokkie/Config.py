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
from typing import Dict, Any, Tuple, Optional
from toktokkie.exceptions import MissingConfig, InvalidConfig
from puffotter.prompt import prompt


class Config:
    """
    Class that handles the loading and saving of configuration data
    """

    config_dir = os.path.join(os.path.expanduser("~"), ".config/toktokkie")
    config_file = os.path.join(config_dir, "config.json")
    keys = {
        "qbittorrent_url": str,
        "qbittorrent_user": str,
        "qbittorrent_password": str,
        "qbittorrent_downloads_dir": str
    }

    def __init__(self, config_data: Optional[Dict[str, Any]] = None):
        """
        Initializes the config object
        :param config_data: If specified, uses this dictionary instead of
                            the data in the config file
        """

        if not os.path.isdir(self.config_dir):
            os.makedirs(self.config_dir)

        if config_data is not None:
            self.config_data = config_data
        elif os.path.isfile(self.config_file):
            with open(self.config_file, "r") as f:
                self.config_data = json.load(f)
        else:
            raise MissingConfig()

        for key in self.keys:
            if key not in self.config_data:
                raise InvalidConfig()

    @classmethod
    def initialize(cls) -> "Config":
        """
        Initializes the config data by prompting the user
        :return: The resulting Config object
        """
        config_data = {}
        for key, _type in cls.keys.items():
            config_data[key] = prompt(key, _type=_type, required=True)
        config = cls(config_data)
        config.save()
        return config

    def save(self):
        """
        Saves the config data to the config file
        :return: None
        """
        with open(self.config_file, "w") as f:
            json.dump(self.config_data, f, indent=4)

    @property
    def qbittorrent_config(self) -> Tuple[str, str, str, str]:
        """
        :return: The qbittorrent config as a tuple of URL, user and password
        """
        return self.config_data["qbittorrent_url"], \
            self.config_data["qbittorrent_user"], \
            self.config_data["qbittorrent_password"], \
            self.config_data["qbittorrent_downloads_dir"]

    @qbittorrent_config.setter
    def qbittorrent_config(self, config: Tuple[str, str, str, str]):
        """
        Sets the qbittorrent config
        :param config: The qbittorrent config as a tuple of URL,
                       user and password
        :return: None
        """
        for index, key in enumerate([
            "qbittorrent_url",
            "qbittorrent_user",
            "qbittorrent_password",
            "qbittorrent_downloads_dir"
        ]):
            self.config_data[key] = config[index]
