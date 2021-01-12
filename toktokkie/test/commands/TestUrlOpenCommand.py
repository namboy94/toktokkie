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

from typing import List
from unittest.mock import patch
from toktokkie.test.TestFramework import _TestFramework


class TestUrlOpenCommand(_TestFramework):
    """
    Tests the url-open command
    """

    history: List[List[str]] = []
    """
    Stores external call history
    """

    def cleanup(self):
        """
        Clears command history
        :return: None
        """
        super().cleanup()
        TestUrlOpenCommand.history = []

    @staticmethod
    def store_history(args: List[str]):
        """
        Adds new entry to history
        :param args: The entry to add
        :return: None
        """
        TestUrlOpenCommand.history.append(args)

    def test_opening_urls(self):
        """
        Tests opening URLS
        :return: None
        """
        with patch("toktokkie.commands.url_open.call", self.store_history):
            self.execute_command(
                ["url-open", self.get("Faust")],
                []
            )
        self.assertEqual(
            self.history,
            [["xdg-open", "https://isbnsearch.org/isbn/9783150000014"]]
        )

    def test_opening_tv_urls(self):
        """
        Tests opening TV URls
        :return: None
        """
        with patch("toktokkie.commands.url_open.call", self.store_history):
            self.execute_command(
                ["url-open", self.get("Fullmetal Alchemist")],
                []
            )
        urls = [
            "https://www.thetvdb.com/?id=75579&tab=series",
            "https://www.imdb.com/title/tt0421357",
            "https://myanimelist.net/anime/121",
            "https://myanimelist.net/anime/664",
            "https://myanimelist.net/anime/430",
            "https://anilist.co/anime/121",
            "https://anilist.co/anime/664",
            "https://anilist.co/anime/430"
        ]
        self.assertEqual(self.history, [["xdg-open", url] for url in urls])

    def test_opening_music_urls(self):
        """
        Tests opening music URls
        :return: None
        """
        with patch("toktokkie.commands.url_open.call", self.store_history):
            self.execute_command(
                ["url-open", self.get("Aimer")],
                []
            )
        urls = [
            "https://musicbrainz.org/artist/"
            "9388cee2-7d57-4598-905f-106019b267d3",
            "https://myanimelist.net/anime/22297",
            "https://myanimelist.net/anime/37521",
            "https://anilist.co/anime/19603",
            "https://anilist.co/anime/101348"
        ]
        self.assertEqual(self.history, [["xdg-open", url] for url in urls])

    def test_opening_book_series(self):
        """
        Tests opening book series URls
        :return: None
        """
        with patch("toktokkie.commands.url_open.call", self.store_history):
            self.execute_command(
                ["url-open", self.get("Bluesteel Blasphemer")],
                []
            )
        urls = [
            "https://isbnsearch.org/isbn/test",
            "https://isbnsearch.org/isbn/test2",
            "https://myanimelist.net/manga/88682",
            "https://anilist.co/manga/98530"
        ]
        self.assertEqual(self.history, [["xdg-open", url] for url in urls])
