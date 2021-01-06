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
from typing import Type
from puffotter.os import listdir
from toktokkie.utils.iconizing.procedures.Procedure import Procedure
from toktokkie.utils.iconizing.procedures.NoopProcedure import NoopProcedure
from toktokkie.utils.iconizing.procedures.GnomeProcedure import GnomeProcedure
from toktokkie.metadata.base.Metadata import Metadata


class Iconizer:
    """
    Class that handles iconizing directories
    """

    all_procedures = [
        GnomeProcedure
    ]
    """
    All implemented procedures
    """

    def __init__(
            self,
            metadata: Metadata,
            procedure: Procedure
    ):
        """
        Initializes the iconizer
        :param metadata: The metadata for the directory to iconize
        :param procedure: The procedure to use for iconizing.
        """
        self.metadata = metadata
        self.procedure = procedure

    def iconize(self):
        """
        Iconizes the directory
        :return: None
        """
        main_path = self.metadata.directory_path
        main_icon = self.metadata.get_icon_file("main")
        self.procedure.iconize(main_path, main_icon)

        for child, child_path in listdir(main_path, no_files=True):
            icon = self.metadata.get_icon_file(child)
            if icon is not None and os.path.isfile(icon):
                self.procedure.iconize(child_path, icon)
            else:
                self.procedure.iconize(child_path, main_icon)

    @staticmethod
    def default_procedure() -> Type[Procedure]:
        """
        Checks all available procedures for eligibility
        :return: The eligible procedure or None if none were found
        """
        for procedure in Iconizer.all_procedures:
            if procedure.is_applicable():
                return procedure
        return NoopProcedure
