
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
from argparse import Namespace
from typing import Dict, Tuple, List

from gfworks.interfaces.GenericWindow import GenericWindow

try:
    from cli.GenericCli import GenericCli
    from modules.hooks.GenericPlugin import GenericPlugin
    from modules.gui.BatchDownloadManagerGui import BatchDownloadManagerGui
    from modules.cli.BatchDownloadManagerCli import BatchDownloadManagerCli
except ImportError:
    from tok_tokkie.cli.GenericCli import GenericCli
    from modules.hooks.GenericPlugin import GenericPlugin
    from modules.gui.BatchDownloadManagerGui \
        import BatchDownloadManagerGui
    from modules.cli.BatchDownloadManagerCli import \
        BatchDownloadManagerCli


class BatchDownloadManagerPlugin(GenericPlugin):
    """
    Class that handles the calls to the Batch Download Manager Plugin.

    It offers methods to start the plugin in CLI-args, CLI-interactive and GUI mode
    """

    def get_name(self) -> str:
        """
        This method returns the name of the Plugin for display purposes

        :return: the name of this plugin
        """
        return "Batch Download Manager"

    def get_config_tag(self) -> str:
        """
        This method returns the tag used to enable or disable this plugin
        in the config file of media-manager.

        :return: the config tag of this plugin
        """
        return "batch-download"

    def get_command_name(self) -> str:
        """
        This method return the command name used by the argument parser
        when using the argument-driven CLI

        :return: the command that starts this plugin
        """
        return "batch-download"

    def get_parser_arguments(self) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        """
        This returns all command line arguments to be added to the Argument Parser for this
        plugin. There are two types of arguments: The ones that ask for strings and the others
        that ask for boolean values.

        To separate these, a tuple structure is used. The tuple's first element contains the
        arguments that ask for boolean values, whereas the second element asks for string values

        The tuple elements are lists of dictionaries. The dictionaries contain the actual
        arguments to be used.

        Every dictionary in the list has a 'tag' key that points to the argument used in the
        --argument fashion from the command line as well as a 'desc' key that points to a
        short description of the parameter.

        :return: the tuple of lists of dictionaries described above
        """
        return ([{"tag": "bdlm-defaults", "desc": "Flag to set the batch download manager to use "
                                                  "the default values from the destination directory"},
                 {"tag": "bdlm-use-nibl", "desc": "Use the NIBL pack searcher with the batch download manager"},
                 {"tag": "bdlm-use-intel", "desc": "Use the Intel Haruhichan searcher with the batch download manager"},
                 {"tag": "bdlm-use-xirc", "desc": "Use the ixIrc searcher with the batch download manager"},
                 {"tag": "bdlm-auto-rename", "desc": "Flag that sets if the files should be auto renamed"},
                 {"tag": "bdlm-search", "desc": "Only searches for packs"}
                 ],

                [{"tag": "bdlm-directory", "desc": "The destination directory of the batch download manager"},
                 {"tag": "bdlm-search-term", "desc": "A custom search term for the search xdcc search"},
                 {"tag": "bdlm-showname", "desc": "The show name to be used by the batch download manager"},
                 {"tag": "bdlm-season", "desc": "The season number to be used by the batch download manager"},
                 {"tag": "bdlm-firstepisode", "desc": "The episode number to be used by the batch download manager"},
                 {"tag": "bdlm-download-selection", "desc": "The packs to be downloaded"}
                 ])

    def start_args_parse(self, args: Namespace) -> None:
        """
        Runs the plugin in arg parse mode
        The arguments must have been parsed beforehand by the MainArgsParser class

        :param args: The parsed argument Namespace
        :return: None
        """
        # Checks if combination of arguments is valid
        valid = False
        if getattr(args, "bdlm-directory"):
            if getattr(args, "bdlm_defaults") ^ (getattr(args, "bdlm-showname") and
                                                 getattr(args, "bdlm-season") and
                                                 getattr(args, "bdlm-firstepisode")):
                if getattr(args, "bdlm_use_nibl") ^ \
                        getattr(args, "bdlm_use_intel") ^ \
                        getattr(args, "bdlm_use_xirc"):
                    if getattr(args, "bdlm_search") ^ getattr(args, "bdlm-download-selection"):
                        valid = True

        # IF valid, execute the command
        if valid:
            search_engine = None
            # Get search engine type
            if getattr(args, "bdlm_use_nibl"):
                search_engine = "NIBL.co.uk"
            elif getattr(args, "bdlm_use_intel"):
                search_engine = "intel.haruhichan.com"
            elif getattr(args, "bdlm_use_xirc"):
                search_engine = "ixIRC.com"

            # If we only want to search, set pack_selection to ""
            if getattr(args, "bdlm_search"):
                pack_selection = ""
            # Otherwise to the string passed by the user
            else:
                pack_selection = getattr(args, "bdlm-download-selection")
            if getattr(args, "bdlm_defaults"):
                # Start Batch Download Manager with automatic values
                BatchDownloadManagerCli().mainloop(directory=getattr(args, "bdlm-directory"),
                                                   use_defaults=True,
                                                   search_engine=search_engine,
                                                   auto_rename=getattr(args, "bdlm_auto_rename"),
                                                   download_selection_override=pack_selection)
            else:
                # Start Batch Download Manager with manual values
                BatchDownloadManagerCli().mainloop(directory=getattr(args, "bdlm-directory"),
                                                   use_defaults=False,
                                                   show_name_override=getattr(args, "bdlm-showname"),
                                                   season_number_override=getattr(args, "bdlm-season"),
                                                   first_episode_override=getattr(args, "bdlm-firstepisode"),
                                                   search_engine=search_engine,
                                                   search_term=getattr(args, "bdlm-search-term"),
                                                   auto_rename=getattr(args, "bdlm_auto_rename"),
                                                   download_selection_override=pack_selection)
        else:
            # Otherwise let the user know that the combination is invalid
            print("Invalid argument combination passed")

    def start_cli(self, parent_cli: GenericCli) -> None:
        """
        Starts the CLI of the plugin in interactive mode

        :param parent_cli: the parent cli to which the plugin can return to
        :return: None
        """
        BatchDownloadManagerCli(parent_cli).start()

    def start_gui(self, parent_gui: GenericWindow) -> None:
        """
        Starts the GUI of the plugin

        :param parent_gui: the gui's parent to which the plugin can return to
        :return: None
        """
        # noinspection PyTypeChecker
        BatchDownloadManagerGui(parent_gui).start()
