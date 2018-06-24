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

from typing import Dict, Any
from colorama import Fore, Style
from toktokkie.metadata.Base import Base
from toktokkie.metadata.AnimeSeries import AnimeSeries
from toktokkie.verification.lib.anilist.Cache import Cache as AnilistCache


class Verificator:
    """
    Abstract class that defines a verification structure with which media
    directory content can be verified
    """

    applicable_metadata_types = [Base]
    """
    Metadata classes on which this verificator may be executed on
    """

    required_attributes = {}
    """
    A dictionary of attributes required for verification to be able to work
    Should be of form: {"attribute": {"help": "Help Message", "type": str}},
    for example. The parameters 'choices' and 'default' may also be used
    """

    input_function = input
    """
    The function used for user input. May be overridden from the outside,
    which is helpful for testing purposes
    """

    def __init__(self, directory, attributes: Dict[str, Any]):
        """
        Initializes the verificator.
        :param directory: The directory to verify
        :param attributes: Attributes provided for verification
        """
        from toktokkie.Directory import Directory

        if not type(directory.metadata) in self.applicable_metadata_types:
            supported = False
            for metatype in self.applicable_metadata_types:
                if directory.metadata.is_subclass_of(metatype):
                    supported = True

            if not supported:
                raise ValueError("Metadata type not supported")

        for attribute, value in self.required_attributes.items():

            if attribute not in attributes:
                raise ValueError("Attribute missing: " + attribute)

        for attribute, value in attributes.items():

            if attribute not in self.required_attributes:
                continue

            type_check = issubclass(
                type(value),
                self.required_attributes[attribute]["type"]
            )

            if not type_check:
                raise ValueError(
                    "Attribute " + attribute + " has wrong type: " +
                    str(type(value)) + ".  Should be: " +
                    self.required_attributes[attribute]
                )

        self.directory = directory  # type: Directory
        self.attributes = attributes

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
    def print_inf(string: str):
        """
        Prints an info string in blue
        :param string: The string to print
        :return: None
        """
        print(Fore.LIGHTBLUE_EX + string + Style.RESET_ALL)

    def prompt(self, prompt: str) -> str:
        """
        Prompts the user for input using yellow text
        :param prompt: The text to prompt the user
        :return: the user prompt
        """
        return self.input_function(
            Fore.YELLOW + prompt + Style.RESET_ALL + "    "
        )

    def prompt_yn(self, prompt: str) -> bool:
        """
        Prompts the user a yes/no question
        :param prompt: The prompt to show the used
        :return: True if the user selected yes, False if no
        """
        response = ""
        while response not in ["y", "n"]:
            response = self.prompt(prompt)
        return response == "y"


# noinspection PyAbstractClass
class AnilistVerificator(Verificator):
    """
    A Verificator class specifically for use with anilist.co related checks.
    """

    applicable_metadata_types = [AnimeSeries]
    """
    By default, only activate for anime series, not for anime movies.
    Support for anime movies will have to be activated separately
    """

    required_attributes = {
        "anilist_user": {
            "type": str,
            "help": "The anilist.co username to use for checks"
        }
    }
    """
    Specifies that the attribute 'anilist_user' is required
    """

    def __init__(self, directory, attributes: Dict[str, Any]):
        """
        Initializes the verificator and adds a couple of
        anilist-specific instance variables.
        :param directory: The directory to verify
        :param attributes: Attributes provided for verification
        """
        super().__init__(directory, attributes)
        self.username = attributes["anilist_user"]
        self.handler = AnilistCache.get_handler_for_user(self.username)
        self.entries = self.handler.entries