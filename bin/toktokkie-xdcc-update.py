#!/usr/bin/env python

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

import argparse
from toktokkie.renaming import schemes, agents, Plex, TVDB
from toktokkie import Directory


def main():
    """
    The toktokkie-xdcc-update main method
    :return: None
    """
    naming_schemes = list(map(lambda x: x.name, schemes))
    naming_agents = list(map(lambda x: x.name, agents))
    default_scheme = Plex.name
    default_agent = TVDB.name

    parser = argparse.ArgumentParser()
    parser.add_argument("directories", nargs="+",
                        help="The directories to xdcc-update. "
                             "Files and directories that do not contain any "
                             "valid metadata configuration will be ignored.")
    parser.add_argument("scheme", choices=set(naming_schemes), nargs="?",
                        default=default_scheme,
                        help="The naming scheme to use")
    parser.add_argument("agent", choices=set(naming_agents), nargs="?",
                        default=default_agent,
                        help="The episode data fetching agent to use")
    parser.add_argument("-c", "--create", action="store_true",
                        help="If set, will prompt for information and create "
                             "new xdcc update instructions")
    args = parser.parse_args()

    directories = args.directories
    scheme = list(filter(lambda x: x.name == args.scheme, schemes))[0]
    agent = list(filter(lambda x: x.name == args.agent, agents))[0]

    for path in directories:

        try:
            directory = Directory(path)

            if args.create:
                directory.create_xdcc_update()
            else:
                directory.xdcc_update(scheme, agent)

        except ValueError:
            print("Updating of " + path + "failed")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Thanks for using toktokkie!")
