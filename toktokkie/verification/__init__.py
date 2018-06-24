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

from typing import List
from toktokkie.metadata import metadata_types, Base
from toktokkie.verification.Verificator import Verificator
from toktokkie.verification.FolderIconVerificator import FolderIconVerificator
from toktokkie.verification.SeasonMetadataVerificator import \
    SeasonMetadataVerificator


all_verificators = [
    FolderIconVerificator,
    SeasonMetadataVerificator
]


def get_verificators(directory,
                     anilist_user: str = None,
                     mal_user: str = None) -> List[Verificator]:
    """
    Retrieves a list of initialized verificators for a directory
    :param directory: The directory to get the verificators for
    :param anilist_user: The anilist.co username used for checks
    :param mal_user: The myanimelist.net username used for checks
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
            verificators.append(
                verificator_type(directory, anilist_user, mal_user)
            )

    return verificators
