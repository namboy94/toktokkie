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
from typing import Dict, Any, List
from puffotter.prompt import prompt_comma_list
from toktokkie.neometadata.enums import IdType
from toktokkie.neometadata.base.MetadataBase import MetadataBase
from toktokkie.neometadata.utils.ids import int_id_types, objectify_ids


class Prompter(MetadataBase, ABC):
    """
    Class that's responsible for defining the metadata creation prompts
    """

    id_prompt_order = [
        IdType.TVDB,
        IdType.IMDB,
        IdType.ISBN,
        IdType.VNDB,
        IdType.MUSICBRAINZ_ARTIST,
        IdType.MUSICBRAINZ_RELEASE,
        IdType.MUSICBRAINZ_RECORDING,
        IdType.MYANIMELIST,
        IdType.ANILIST,
        IdType.KITSU,
        IdType.MANGADEX
    ]
    """
    The order in which ID types should be prompted
    """

    @classmethod
    def prompt(cls, directory_path: str) -> Dict[str, Any]:
        """
        Generates a new Metadata object using prompts for a directory
        :param directory_path: The path to the directory for which to generate
                               the metadata object
        :return: The generated metadata object
        """
        name = os.path.basename(os.path.abspath(directory_path))
        print(f"Generating metadata for {name}:")
        data = {
            "type": cls.media_type().value,
            "tags": prompt_comma_list("Tags"),
            "ids": cls._prompt_ids(
                cls.valid_id_types(), cls.required_id_types(), {}
            )
        }
        return data

    @classmethod
    def _prompt_ids(
            cls,
            valid_ids: List[IdType],
            required_ids: List[IdType],
            defaults: Dict[str, List[str]],
            mincount: int = 1
    ) -> Dict[str, List[str]]:
        """
        Prompts the user for any valid IDs the metadata may contain
        :param valid_ids: IDs that are valid for the prompt
        :param required_ids: IDs that are required to be provided
        :param defaults: Any potential default values for the IDs
        :param mincount: Minimal amount of IDs that the user needs to provide
        :return: The IDs in a dictionary mapping the ID names to their IDs
        """
        ids = {}  # type: Dict[str, List[str]]
        for id_type in cls.id_prompt_order:
            if id_type not in valid_ids:
                continue
            else:
                defaults = cls._load_default_ids(valid_ids, defaults)

                default = defaults.get(id_type.value)
                is_int = id_type in int_id_types

                min_count = 0
                if id_type in required_ids:
                    min_count = 1

                prompted = prompt_comma_list(
                    "{} IDs".format(id_type.value),
                    min_count=min_count,
                    default=default,
                    primitive_type=int if is_int else lambda x: str(x)
                )
                prompted = [str(x) for x in prompted]
                non_default = prompted != default

                if len(prompted) > 0:
                    ids[id_type.value] = prompted
                    defaults[id_type.value] = prompted

                    # Update anilist IDs if myanimelist IDs were updated
                    if id_type == IdType.MYANIMELIST and non_default:
                        if IdType.ANILIST.value in defaults:
                            defaults.pop(IdType.ANILIST.value)

        if len(ids) < mincount:
            print("Please enter at least {} IDs".format(mincount))
            return cls._prompt_ids(
                valid_ids, required_ids, defaults, mincount
            )
        else:
            return ids

    @classmethod
    def _load_default_ids(
            cls,
            valid_ids: List[IdType],
            defaults: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Tries to load any missing default IDs using the name of the directory
        and/or other default IDs
        :param valid_ids: List of valid ID types
        :param defaults: The current default IDs
        :return: The updated IDs
        """
        for id_type in valid_ids:
            if id_type.value in defaults:
                continue
            else:
                _defaults = objectify_ids(defaults)
                ids = cls.id_fetcher.fetch_ids(id_type, _defaults)
                if ids is not None:
                    defaults[id_type.value] = ids

        return defaults

    @classmethod
    def _prompt_component_ids(
            cls,
            valid_ids: List[IdType],
            previous_ids: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Prompts for IDs for a component (for example, a season of a tv series)
        Strips away any IDs that are the same as the root metadata ids
        :param valid_ids: ID Types that are valid for the kind of metadata
        :param previous_ids: The IDs previously aquired
        :return: The prompted IDs, mapped to id type strings
        """

        defaults = previous_ids.copy()
        ids = cls._prompt_ids(valid_ids, [], defaults, 0)

        # Strip unnecessary IDs
        for key in list(ids.keys()):
            value = ids[key]
            if previous_ids.get(key) == value:
                ids.pop(key)

        return ids
