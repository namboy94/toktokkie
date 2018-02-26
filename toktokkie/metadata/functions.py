"""
Copyright 2015-2018 Hermann Krumrey <hermann@krumreyh.com>

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
"""

from toktokkie.metadata.Base import Base


def get_metadata_types() -> list:
    """
    Retrieves a list of all available metadata types
    :return: The list of metadata types
    """
    return[Base]


def prompt_user(arg: str, arg_type: any, default: object = None) \
        -> any:
    """
    Prompts a user for input.
    :param arg: The argument which the user is prompted for
    :param arg_type: The argument's type
    :param default: An optional default value,
                    used when the user enters nothing
    :return: The result of the prompt
    """

    prompt = arg + " "
    if default is not None:
        prompt += "(Default: " + str(default) + ")"
    prompt += ":   "

    while True:
        response = input(prompt)
        if not response and default is None:
            continue
        elif not response and default is not None:
            return default
        else:
            try:
                return arg_type(response)
            except ValueError:
                continue
