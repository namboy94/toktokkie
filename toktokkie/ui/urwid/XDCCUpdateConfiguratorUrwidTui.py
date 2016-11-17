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
from toktokkie.utils.xdcc.updating.JsonHandler import JsonHandler
from toktokkie.utils.xdcc.updating.AutoSearcher import AutoSearcher
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager


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

        self.loop = None
        self.top = None
        self.list_walker = None

        self.json_handler = JsonHandler()

        self.title_text = urwid.Text("XDCC Update Configurator")

        self.json_file_location = urwid.Edit(caption="JSON File: ")
        self.open_button = urwid.Button("Open JSON file")
        self.save_button = urwid.Button("Save JSON file")

        self.series = []
        self.new_series_button = urwid.Button("New Series")
        self.delete_series_button = urwid.Button("Delete selected Series")

        self.configuration_header = urwid.Text("Series Configuration")
        self.series_directory_edit = urwid.Edit("Directory:   ")
        self.search_name_edit = urwid.Edit("Search Name: ")
        self.bot_edit = urwid.Edit("Bot:         ")
        self.season_edit = urwid.IntEdit("Season:      ")

        self.quality_selector_title = urwid.Text("Quality:")
        self.quality_selectors = []
        for quality in ["480p", "720p", "1080p"]:
            urwid.RadioButton(self.quality_selectors, quality)

        self.search_engine_title = urwid.Text("Search Engine: ")
        self.search_engines = []
        for engine in PackSearcher.get_available_pack_searchers():
            urwid.RadioButton(self.search_engines, engine)

        self.naming_scheme_title = urwid.Text("Naming Schemes:")
        self.naming_schemes = []
        for scheme in SchemeManager.get_scheme_names():
            urwid.RadioButton(self.naming_schemes, scheme)

        self.naming_pattern_title = urwid.Text("Naming Pattern")
        self.naming_patterns = []
        for pattern in AutoSearcher.get_available_patterns():
            urwid.RadioButton(self.naming_patterns, pattern)

        self.confirm_button = urwid.Button("Confirm Changes")

        self.lay_out()

    def lay_out(self) -> None:
        """
        Handles the layout of the TUI elements

        :return: None
        """
        div = urwid.Divider()

        open_button = urwid.AttrMap(self.open_button, None, focus_map='reversed')
        save_button = urwid.AttrMap(self.save_button, None, focus_map='reversed')
        new_series_button = urwid.AttrMap(self.new_series_button, None, focus_map='reversed')
        delete_series_button = urwid.AttrMap(self.delete_series_button, None, focus_map='reversed')
        confirm_button = urwid.AttrMap(self.confirm_button, None, focus_map='reversed')

        self.upper_body = [self.title_text, div, self.json_file_location, open_button, save_button, div]
        self.lower_body = [new_series_button, delete_series_button, div, self.configuration_header,
                           self.series_directory_edit, self.search_name_edit, self.bot_edit, self.season_edit]
        self.lower_body += [self.quality_selector_title] + self.quality_selectors
        self.lower_body += [self.search_engine_title] + self.search_engines
        self.lower_body += [self.naming_scheme_title] + self.naming_schemes
        self.lower_body += [self.naming_pattern_title] + self.naming_patterns
        self.lower_body += [confirm_button]

        self.list_walker = urwid.SimpleFocusListWalker(self.upper_body + self.lower_body)
        self.top = urwid.Overlay(urwid.Padding(urwid.ListBox(self.list_walker), left=2, right=2),
                                 urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                                 align='center', width=('relative', 80),
                                 valign='middle', height=('relative', 70),
                                 min_width=20, min_height=10)

    def start(self) -> None:  # pragma: no cover
        """
        Starts the TUI

        :return: None
        """
        self.loop = urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')])
        self.loop.run()

    # noinspection PyMethodMayBeStatic
    def quit(self) -> None:
        """
        Cleans up any variables that may cause thread to continue executing after the TUI ends

        :return: None
        """
        pass
