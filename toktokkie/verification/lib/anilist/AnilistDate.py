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


class AnilistDate:
    """
    Class that models a date
    """

    def __init__(self, year: int, month: int, day: int):
        """
        Initializes the date object
        :param year: The year
        :param month: The month
        :param day: The day
        """
        self.year = year
        self.month = month
        self.day = day

    def valid(self) -> bool:
        """
        Queries if the date is valid, i.e. completely filled out
        :return: True if complete, False otherwise
        """
        return self.year is not None \
            and self.month is not None \
            and self.day is not None
