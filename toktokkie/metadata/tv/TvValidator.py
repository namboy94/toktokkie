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
from abc import ABC
from typing import Dict, Any
from puffotter.os import listdir
from toktokkie.exceptions import InvalidMetadata
from toktokkie.metadata.base.Validator import Validator
from toktokkie.metadata.tv.TvExtras import TvExtras


class TvValidator(Validator, TvExtras, ABC):
    """
    Class that handles validation of tv series metadata
    """

    @classmethod
    def build_schema(cls) -> Dict[str, Any]:
        """
        Generates the JSON schema
        :return: The JSON schema
        """
        base = super().build_schema()
        ids = cls._create_ids_schema()

        excludes = {}
        multi_episodes = {}
        season_start_overrides = {}
        for id_type in cls.valid_id_types():
            extra_base = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "season": {"type": "number"},
                        "episode": {"type": "number"}
                    },
                    "required": ["season", "episode"]
                }
            }
            excludes[id_type.value] = extra_base.copy()
            season_start_overrides[id_type.value] = extra_base.copy()

            extra_base = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "season": {"type": "number"},
                        "start_episode": {"type": "number"},
                        "end_episode": {"type": "number"}
                    },
                    "required": ["season", "start_episode", "end_episode"]
                }
            }
            multi_episodes[id_type.value] = extra_base.copy()

        base["properties"].update({
            "seasons": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "ids": ids,
                        "name": {"type": "string"}
                    },
                    "required": ["name"],
                    "additionalProperties": False
                }
            },
            "excludes": {
                "type": "object",
                "additionalProperties": excludes
            },
            "season_start_overrides": {
                "type": "object",
                "additionalProperties": season_start_overrides
            },
            "multi_episodes": {
                "type": "object",
                "additionalProperties": multi_episodes
            }
        })
        base["required"].append("seasons")
        return base

    def validate(self):
        """
        Performs additional validation
        """
        super().validate()
        foldercount = len(listdir(self.directory_path, no_files=True))

        if len(self.seasons) < foldercount:
            raise InvalidMetadata("Missing seasons in metadata")
        elif len(self.seasons) > foldercount:
            raise InvalidMetadata("Missing season directories")

        for season in self.seasons:
            if not os.path.isdir(season.path):
                raise InvalidMetadata("Missing season directory {}"
                                      .format(season.name))
