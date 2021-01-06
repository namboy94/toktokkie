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
from typing import List, Type, Dict, Any
from puffotter.prompt import yn_prompt
from toktokkie.metadata.base.Metadata import Metadata
from toktokkie.utils.update.Updater import Updater
from toktokkie.utils.update.XDCCUpdater import XDCCUpdater
from toktokkie.utils.update.MangadexUpdater import MangadexUpdater
from toktokkie.utils.update.TorrentUpdater import TorrentUpdater
from toktokkie.exceptions import InvalidUpdateInstructions, \
    MissingUpdateInstructions

updaters = [MangadexUpdater, XDCCUpdater, TorrentUpdater]
"""
List of all available updaters
"""


def perform_update(
        args: Dict[str, Any],
        metadata: Metadata,
        applicable_updaters: List[Type[Updater]]
):
    """
    Performs updates on metadata
    :param args: The CLI arguments
    :param metadata: The metadata
    :param applicable_updaters: The applicable updater classes
    :return: None
    """
    if args["create"]:
        to_create = None
        to_delete = []
        if len(applicable_updaters) > 1:
            for updater_cls in applicable_updaters:
                selected = yn_prompt(f"Create update configuration for "
                                     f"{updater_cls.name()}?")
                if selected:
                    if to_create is not None:
                        print("Only one update configuration is allowed")
                        return
                    to_create = updater_cls
                else:
                    to_delete.append(updater_cls)
        else:
            to_create = applicable_updaters[0]

        if to_create is None:
            print("No update instructions created")
        else:
            to_create.prompt(metadata)
            for cls in to_delete:
                update_file = cls.update_file(metadata.directory_path)
                if os.path.isfile(update_file):
                    os.remove(update_file)

    else:
        has_instructions = []
        for updater_cls in applicable_updaters:
            if updater_cls.json_schema() is None:
                has_instructions.append(updater_cls)
            update_file = updater_cls.update_file(metadata.directory_path)
            if os.path.isfile(update_file):
                has_instructions.append(updater_cls)

        if len(has_instructions) == 0:
            print("No Update Instructions configured")
        elif len(has_instructions) > 1:
            print("More than one update instructions configured")
        else:
            try:
                updater = has_instructions[0](metadata, args)
                print("Updating {} using {} updater:".format(
                    metadata.name, updater.name()
                ))
                updater.update()
            except MissingUpdateInstructions:
                print("No update instructions for {}".format(metadata.name))
            except InvalidUpdateInstructions as e:
                print(
                    "Update instructions for {} are invalid: {}"
                    .format(metadata.name, e)
                )
