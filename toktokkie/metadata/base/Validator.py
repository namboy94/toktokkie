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
from typing import Dict, Any, List, Optional
from jsonschema import validate, ValidationError
from toktokkie.enums import IdType
from toktokkie.exceptions import InvalidMetadata
from toktokkie.metadata.base.MetadataBase import MetadataBase


class Validator(MetadataBase, ABC):
    """
    Class that handles validation of metadata
    """

    def validate(self):
        """
        Validates the JSON data to make sure everything has valid values
        :raises InvalidMetadataException: If any errors were encountered
        :return: None
        """
        try:
            validate(instance=self.json, schema=self.build_schema())
        except ValidationError as e:
            raise InvalidMetadata(
                "Invalid Metadata: {} ({})".format(e, e.message)
            )

    @classmethod
    def build_schema(cls) -> Dict[str, Any]:
        """
        Generates the JSON schema
        :return: The JSON schema
        """
        ids = cls._create_ids_schema()
        ids["minProperties"] = 1

        properties = {
            "tags": {
                "type": "array",
                "items": {"type": "string"}
            },
            "ids": ids,
            "type": {
                "type": "string",
                "pattern": "^" + str(cls.media_type().value) + "$"
            }
        }
        required = ["type", "ids"]

        return {
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False
        }

    @classmethod
    def _create_ids_schema(
            cls, valid_id_type_overrides: Optional[List[IdType]] = None
    ) -> Dict[str, Any]:
        """
        Creates an "ids" object that allows any valid ID types
        :return: The "ids" object in JSON schema format
        """
        id_types = cls.valid_id_types()
        if valid_id_type_overrides is not None:
            id_types = valid_id_type_overrides

        properties = {}  # type: Dict[str, Any]
        for id_type in id_types:
            properties[id_type.value] = {
                "type": "array",
                "items": {"type": "string"}
            }

        return {
            "type": "object",
            "properties": properties,
            "additionalProperties": False,
            "required": [x.value for x in cls.required_id_types()]
        }
