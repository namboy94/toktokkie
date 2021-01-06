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


class Procedure:
    """
    Interface that defines the methods an iconizing procedure must provide
    """

    name = "procedure"
    """
    The name/identifier of the procedure
    """

    @classmethod
    def iconize(cls, directory: str, png_icon_path: str):
        """
        Iconizes a directory with an icon file
        :param directory: The directory to iconize
        :param png_icon_path: The path to the png icon file
        :return: None
        """
        raise NotImplementedError()

    @classmethod
    def is_applicable(cls) -> bool:
        """
        Checks if this procedure is applicable to the current system
        :return: True if applicable, else False
        """
        raise NotImplementedError()
