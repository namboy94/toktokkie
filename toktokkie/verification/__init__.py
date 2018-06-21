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


all_verificators = [
    FolderIconVerificator
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

    try:
        verificators = {}
        for metadata_type in metadata_types:
            verificators[metadata_type.type] = list(filter(
                lambda x: metadata_type in x.applicable_metadata_types,
                all_verificators
            ))

        return list(map(
            lambda x: x(directory, anilist_user, mal_user),
            verificators[metadata.type]
        ))
    except KeyError:
        return []
