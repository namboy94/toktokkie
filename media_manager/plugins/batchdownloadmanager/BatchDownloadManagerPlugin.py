"""
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
"""

try:
    from plugins.common.GenericPlugin import GenericPlugin
    from plugins.batchdownloadmanager.userinterfaces.BatchDownloadManagerGUI import BatchDownloadManagerGUI
    from plugins.batchdownloadmanager.userinterfaces.BatchDownloadManagerCli import BatchDownloadManagerCli
except ImportError:
    from media_manager.plugins.common.GenericPlugin import GenericPlugin
    from media_manager.plugins.batchdownloadmanager.userinterfaces.BatchDownloadManagerGUI \
        import BatchDownloadManagerGUI
    from media_manager.plugins.batchdownloadmanager.userinterfaces.BatchDownloadManagerCli import \
        BatchDownloadManagerCli


class BatchDownloadManagerPlugin(GenericPlugin):
    """
    Class that handles the calls to the BatchDownloadManager
    """

    def get_name(self):
        """
        :return: "Batch Download Manager"
        """
        return "Batch Download Manager"

    def get_config_tag(self):
        """
        :return: "batch-download"
        """
        return "batch-download"

    def get_command_name(self):
        """
        :return: "batch download"
        """
        return "batch-download"

    def get_parser_arguments(self):
        """
        :return: tuple of two list of dictionaries, consisting of argument tags and descriptions.
                    the first tuple element contains boolean values, the others store string values
        """
        return ([{"tag": "bdlm-defaults", "desc": "Flag to set the batch download manager to use "
                                                  "the default values from the destination directory"},
                 {"tag": "bdlm-showname", "desc": "The show name to be used by the batch download manager"},
                 {"tag": "bdlm-season", "desc": "The season number to be used by the batch download manager"},
                 {"tag": "bdlm-firstepisode", "desc": "The episode number to be used by the batch download manager"},
                 {"tag": "bdlm-use-nibl", "desc": "Use the NIBL pack searcher with the batch download manager"},
                 {"tag": "bdlm-use-intel", "desc": "Use the Intel Haruhichan searcher with the batch download manager"},
                 {"tag": "bdlm-use-xirc", "desc": "Use the xIrc searcher with the batch download manager"}],

                [{"tag": "bdlm-directory", "desc": "The destination directory of the batch download manager"}])

    def start_args_parse(self, args):
        """
        Runs the plugin in arg parse mode
        """
        valid = False
        if getattr(args, "bdlm-directory"):
            if getattr(args, "bdlm-defaults") ^ (getattr(args, "bdlm-showname") and
                                                 getattr(args, "bdlm-season") and
                                                 getattr(args, "bdlm-firstepisode")):
                if getattr(args, "bdlm-use-nibl") ^ \
                        getattr(args, "bdlm-use-intel") ^ \
                        getattr(args, "bdlm-use-xirc"):
                    valid = True

        if valid:
            print("Do Stuff")
        else:
            print("Invalid argument combination passed")

    def start_cli(self, parent_cli):
        """
        Starts the CLI of the plugin
        :param parent_cli: the parent cli
        :return: void
        """
        BatchDownloadManagerCli(parent_cli).start()

    def start_gui(self, parent_gui):
        """
        Starts the GUI, while hiding the parent until finished
        :param parent_gui: the parent gui window
        :return: void
        """
        BatchDownloadManagerGUI(parent_gui).start()
