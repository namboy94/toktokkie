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
from typing import List
from toktokkie.neometadata.base.MetadataBase import MetadataBase
from toktokkie.neometadata.renaming.RenameOperation import RenameOperation


class Renamer(MetadataBase, ABC):
    """
    Class that's responsible to define renaming functionality
    """

    def resolve_title_name(self) -> str:
        """
        If possible, will fetch the appropriate name for the
        metadata based on IDs, falling back to the
        directory name if this is not possible or supported.
        """
        return self.name

    # noinspection PyMethodMayBeStatic
    def create_rename_operations(self) -> List[RenameOperation]:
        """
        Performs rename operations on the content referenced by
        this metadata object
        :return: The rename operations for this metadata
        """
        return []
