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

from colorama import Fore, Style
from toktokkie.metadata.Base import Base


class Verificator:
    """
    Abstract class that defines a verification structure with which media
    directory content can be verified
    """

    applicable_metadata_types = [Base]
    """
    Metadata classes on which this verificator may be executed on
    """

    def __init__(self, directory,
                 anilist_user: str = None,
                 mal_user: str = None):
        """
        Initializes the verificator.
        :param directory: The directory to verify
        :param anilist_user: The anilist.co username used for checks
        :param mal_user: The myanimelist.net username used for checks
        """
        from toktokkie.Directory import Directory

        if not type(directory.metadata) in self.applicable_metadata_types:
            supported = False
            for metatype in self.applicable_metadata_types:
                if directory.metadata.is_subclass_of(metatype):
                    supported = True

            if not supported:
                raise ValueError("Metadata type not supported")

        self.directory = directory  # type: Directory
        self.anilist_user = anilist_user
        self.mal_user = mal_user

    def verify(self) -> bool:
        """
        Checks if the media directory has no issues.
        If it does, this method will return False.
        Issues may be fixed using the fix() method.
        :return: True if no issues were found, False otherwise
        """
        raise NotImplementedError()

    def fix(self):
        """
        Allows the user to fix the issue using prompts
        :return: None
        """
        raise NotImplementedError()

    @staticmethod
    def print_err(string: str):
        """
        Prints an error message in red
        :param string: The message to print
        :return: None
        """
        print(Fore.RED + string + Style.RESET_ALL)

    @staticmethod
    def print_ins(string: str):
        """
        Prints an instruction message in white
        :param string: The message to print
        :return: None
        """
        print(Fore.WHITE + string + Style.RESET_ALL)

    @staticmethod
    def prompt(prompt: str) -> str:
        """
        Prompts the user for input using yellow text
        :param prompt: The text to prompt the user
        :return: the user prompt
        """
        return input(Fore.YELLOW + prompt + Style.RESET_ALL + "    ")

    @staticmethod
    def prompt_yn(prompt: str) -> bool:
        """
        Prompts the user a yes/no question
        :param prompt: The prompt to show the used
        :return: True if the user selected yes, False if no
        """
        response = ""
        while response not in ["y", "n"]:
            response = Verificator.prompt(prompt)
        return response == "y"
