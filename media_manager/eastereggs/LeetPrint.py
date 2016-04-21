"""
LICENSE:

Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.

LICENSE
"""

# imports
import sys
import builtins
from typing import Dict


class LeetPrint(object):
    """
    Class that replaces the standard print function with a customized one using leet speak
    """

    simple_leet = {"a": "4", "A": "4",
                   "b": "8", "B": "8",
                   "e": "3", "E": "3",
                   "g": "9", "G": "6",
                   "i": "!", "I": "!",
                   "l": "1", "L": "1",
                   "o": "0", "O": "0",
                   "s": "5", "S": "5",
                   "t": "7", "T": "7"}
    """
    Dictionary implementing a very barebones form of leet, not using multi-character replacements
    """

    @staticmethod
    def activate_leet(simple: bool = True) -> None:
        """
        Activates Leet Speak by replacing the builtin print function

        :param simple: Only use the simple 1337 leetspeak
        :return: None
        """

        def leetspeak_generator(dictionary: Dict[str, str]) -> callable:
            """
            Generates a method that converts a string into leetspeak.

            The leetspeek implementation can be defined via a dictionary (in theory, you could
            use any dictionary, but this class is meant to turn it into leetspeak)

            The generated method can then be used to replace the builtin print method

            :param dictionary: The dictionary used to
            """

            def generated_method(string: str = "", end="\n"):
                """
                The generated method that emulates print's functionality while replacing
                characters from the string with the ones defined in the dictionary

                :param string: the string to print
                :param end: the end of the string to print, defaults to newline
                :return: None
                """

                print_string = string

                # Iterate over all letter in dictionary
                for key in dictionary:
                    print_string = print_string.replace(key, dictionary[key])  # Replace the characters

                sys.stdout.write(print_string + end)  # Write the new string to stdout

            # Return the generated method
            return generated_method

        if simple:
            # Replace the builtin print method if using python 3
            builtins.print = leetspeak_generator(LeetPrint.simple_leet)
