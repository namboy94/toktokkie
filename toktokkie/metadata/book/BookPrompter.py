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
from puffotter.os import listdir
from toktokkie.metadata.base.Prompter import Prompter
from toktokkie.metadata.book.BookExtras import BookExtras
from toktokkie.exceptions import InvalidDirectoryState


class BookPrompter(Prompter, BookExtras, ABC):
    """
    Implements the Prompter functionality for book metadata
    """

    @classmethod
    def pre_prompt_check(cls, directory_path: str):
        """
        Makes sure that the book directory has exactly one book file
        :param directory_path: The path to the directory to check
        :return: None
        """
        super().pre_prompt_check(directory_path)
        filecount = len(listdir(directory_path, no_dirs=True))
        if filecount == 0:
            raise InvalidDirectoryState("No book file")
        elif filecount > 1:
            raise InvalidDirectoryState("More than one book file")
