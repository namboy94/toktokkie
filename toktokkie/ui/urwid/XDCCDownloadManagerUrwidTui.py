"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

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
LICENSE
"""

# imports
import os
import urwid
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager
from toktokkie.utils.xdcc.XDCCDownloadManager import XDCCDownloadManager
from toktokkie.utils.iconizing.procedures.ProcedureManager import ProcedureManager


class XDCCDownloadManagerUrwidTui(object):
    """
    Urwid TUI for the XDCC Download Manager functionality
    """

    def __init__(self) -> None:
        """
        Initializes the TUI's various widgets
        """

        self.upper_body = []
        self.middle_body = []
        self.lower_body = []

        self.top = None
        self.list_walker = None

        self.title = urwid.Text("XDCC Download Manager")
        self.target_directory_edit = urwid.Edit("Target Directory:")
        self.target_directory_edit.set_edit_text(os.getcwd())
        self.series_name_edit = urwid.Edit("Series Name:")
        self.season_number_edit = urwid.Edit("Season Number:")
        self.episode_number_edit = urwid.Edit("Episode Number:")

        self.renaming_schemes = []
        for scheme in SchemeManager.get_scheme_names():
            urwid.RadioButton(self.renaming_schemes, scheme)
        self.rename_check = urwid.CheckBox("Auto-rename", state=True)

        self.iconizing_procedures = []
        for procedure in ProcedureManager.get_procedure_names():
            urwid.RadioButton(self.iconizing_procedures, procedure)
        self.iconize_check = urwid.CheckBox("Iconize", state=True)

        self.search_term_edit = urwid.Edit("Search Term:")
        self.search_engines = []
        for engine in ["All"] + PackSearcher.get_available_pack_searchers():
            urwid.RadioButton(self.search_engines, engine)

        self.search_button = urwid.Button("Search")

        self.search_results = []
        self.search_result_radios = []

        self.download_button = urwid.Button("Download")

        self.single_progress_bar = urwid.ProgressBar("Single N", "Single C")
        self.total_progress_bar = urwid.ProgressBar("Total N", "Total N")
        self.current_speed = urwid.Text("Current Speed:")
        self.average_speed = urwid.Text("Average Speed:")

        self.lay_out()
        self.connect_widgets()

    def lay_out(self) -> None:
        """
        Handles the layout of the TUI elements

        :return: None
        """
        div = urwid.Divider()

        self.upper_body = [self.title, div, self.target_directory_edit, self.series_name_edit, self.season_number_edit]
        self.upper_body += [self.episode_number_edit, div] + self.renaming_schemes + [self.rename_check, div]
        self.upper_body += self.iconizing_procedures + [self.iconize_check, div]
        self.upper_body += [self.search_term_edit] + self.search_engines + [self.search_button, div]

        self.lower_body = [div, self.download_button, div, self.single_progress_bar, self.total_progress_bar]
        self.lower_body += [self.current_speed, self.average_speed]

        body = self.upper_body + self.middle_body + self.lower_body

        self.list_walker = urwid.SimpleFocusListWalker(body)
        self.top = urwid.Overlay(urwid.Padding(urwid.ListBox(self.list_walker), left=2, right=2),
                                 urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                                 align='center', width=('relative', 80),
                                 valign='middle', height=('relative', 70),
                                 min_width=20, min_height=10)

    def connect_widgets(self) -> None:
        """
        Connects the various widgets to their functionality

        :return: None
        """
        urwid.connect_signal(self.target_directory_edit, 'change', self.parse_directory)
        urwid.connect_signal(self.search_button, 'click', self.start_search)
        urwid.connect_signal(self.download_button, 'click', self.start_download)

    def start(self) -> None:
        """
        Starts the TUI

        :return: None
        """
        urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')]).run()

    # noinspection PyUnusedLocal
    def parse_directory(self, widget: urwid.Edit, directory: str) -> None:
        """
        Parses the currently entered directory, and fills in the information it can gather from that into the
        relevant UI elements

        :param widget:    The widget that did the method call
        :param directory: The new content of the widget's edit text
        :return:          None
        """
        series_name = os.path.basename(directory)
        season, episode = XDCCDownloadManager.get_max_season_and_episode_number(directory)

        self.series_name_edit.set_edit_text(series_name)
        self.search_term_edit.set_edit_text(series_name)
        self.episode_number_edit.set_edit_text(str(episode))
        self.season_number_edit.set_edit_text(str(season))

    def start_search(self) -> None:
        """
        Starts searching for the XDCC pack specified via the search term and search engines to use

        :return: None
        """
        pass

    def start_download(self) -> None:
        """
        Starts the XDCC download procedure

        :return: None
        """
        pass
