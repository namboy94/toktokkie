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

from typing import List, Dict, Any
from toktokkie.metadata import metadata_types, Base
from toktokkie.verification.Verificator import Verificator
from toktokkie.verification.FolderIconVerificator import FolderIconVerificator
from toktokkie.verification.SeasonMetadataVerificator import \
    SeasonMetadataVerificator
from toktokkie.verification.EpisodeNameVerificator import \
    EpisodeNameVerificator
from toktokkie.verification.EntriesInAnilistVerificator import \
    EntriesInAnilistVerificator
from toktokkie.verification.TVDBEpisodeCountVerificator import \
    TVDBEpisodeCountVerificator


all_verificators = [
    FolderIconVerificator,
    SeasonMetadataVerificator,
    EpisodeNameVerificator,
    EntriesInAnilistVerificator,
    TVDBEpisodeCountVerificator
]
"""
A list of all verificators
"""


def get_verificators(directory, attributes: Dict[str, Any]) \
        -> List[Verificator]:
    """
    Retrieves a list of initialized verificators for a directory
    :param directory: The directory to get the verificators for
    :param attributes: The attributes to use for verification
    :return: The list of verificators
    """

    metadata = directory.metadata  # type: Base

    verificators = []

    applicable = []
    for metadata_type in metadata_types:
        if metadata.is_subclass_of(metadata_type):
            applicable.append(metadata_type)

    for verificator_type in all_verificators:
        valid = False
        for metadata_type in applicable:
            if metadata_type in verificator_type.applicable_metadata_types:
                valid = True

        if valid:
            try:
                verificators.append(
                    verificator_type(directory, attributes)
                )
            except ValueError:  # Ignore failing verificators
                pass

    return verificators


def get_all_verificator_attributes() -> Dict[str, Dict[str, str or type]]:
    """
    Retrieves a dictionary containing info for all available verificator
    attributes.
    :return: The dictionary of verificator attribute info
    """

    attributes = {}

    for verificator in all_verificators:
        for attribute, info in verificator.required_attributes.items():
            attributes[attribute] = info

    return attributes
