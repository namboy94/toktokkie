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
import requests
from bs4 import BeautifulSoup
from typing import List

try:
    from plugins.batchdownloadmanager.searchengines.GenericGetter import GenericGetter
    from plugins.batchdownloadmanager.searchengines.objects.XDCCPack import XDCCPack
except ImportError:
    from media_manager.plugins.batchdownloadmanager.searchengines.GenericGetter import GenericGetter
    from media_manager.plugins.batchdownloadmanager.searchengines.objects.XDCCPack import XDCCPack


class IxIRCGetter(GenericGetter):
    """
    Class that searches the xdcc pack lists from ixirc.com
    """

    def search(self) -> List[XDCCPack]:
        """
        Method that conducts the xdcc pack search. This also automatically finds out the bot and channel
        via web parsing, so the two methods get_channel and get_server are not needed

        :return: the search results as a list of XDCCPack objects
        """

        # Generate search URL.
        # ixIRC.com replaces spaces with + symbols.
        split_search_term = self.search_term.split(" ")
        prepared_search_term = split_search_term[0]
        i = 1
        while i < len(split_search_term):
            prepared_search_term += "+" + split_search_term[i]
            i += 1

        # Check how many pages need to be parsed:
        number_of_pages = 1  # Minimum amount of pages to parse

        # Get information from web page
        base_url = "https://ixirc.com/?q=" + prepared_search_term
        content = BeautifulSoup(requests.get(base_url).text, "html.parser")
        page_analysis = content.select("h3")  # Search all 'h3' elements of the web page

        if "Over" in page_analysis[0].text:
            # If 'Over' is used in the h3 section of the page, it means that this is not the last
            # page with search results. It displays "Over X episodes" on all pages except the last, where
            # the exact amount of results is mentioned and the word 'Over' is omitted
            number_of_pages = 2

        urls = [base_url]

        # Check for more pages and add their URLs t the urls list.
        analysing = False
        if number_of_pages == 2:
            analysing = True
        while analysing:
            # The new URL specifies a page number using &pn=
            url = "https://ixirc.com/?q=" + prepared_search_term + "&pn=" + str(number_of_pages - 1)
            urls.append(url)
            content = BeautifulSoup(requests.get(url).text, "html.parser")
            page_analysis = content.select("h3")
            if "Over" in page_analysis[0].text:
                # Found another page
                number_of_pages += 1
                continue
            else:
                # All pages found
                analysing = False

        # Establish search results
        results = []
        for url in urls:
            self.__get_page_results__(url, results)

        return results

    @staticmethod
    def __get_page_results__(url: str, results: List[XDCCPack]) -> None:
        """
        This parses a single ixIRC page to find all search results from that one URL
        :param url: the URL to parse
        :param results: the list of search results to which these new results will be added to
        :return: None
        """
        # get page info with beautifulsoup
        content = BeautifulSoup(requests.get(url).text, "html.parser")
        # Get the 'td' elements of the page
        packs = content.select("td")

        # Initialize the pack variables
        file_name = ""
        bot = ""
        server = ""
        channel = ""
        pack_number = 0
        size = ""

        line_count = 0
        ago_count = 0
        aborted = False
        next_element = False

        # Holy fuck what the fuck is this fucking shit?
        # TODO make sense of this, comment everything
        for line in packs:
            if next_element and line.text == "":
                continue
            if next_element and not line.text == "":
                next_element = False
            if not next_element and line.text == "":
                aborted = True
            if "ago" in line.text:
                ago_count += 1
            if not aborted:
                if line_count == 0:
                    file_name = line.text
                elif line_count == 1:
                    server = line.text
                elif line_count == 2:
                    channel = line.text
                elif line_count == 3:
                    bot = line.text
                elif line_count == 4:
                    pack_number = int(line.text)
                elif line_count == 6:
                    size = line.text
            if not aborted and ago_count == 2:
                ago_count = 0
                line_count = 0
                next_element = True
                result = XDCCPack(file_name, "irc." + server + ".net", channel, bot, pack_number, size)
                results.append(result)
            if aborted and ago_count == 2:
                aborted = False
                ago_count = 0
                line_count = 0
                next_element = True
            if not next_element:
                line_count += 1

    def get_server(self, bot: str) -> str:
        """
        Checks to which server a given xdcc-serving bot belongs to.

        :param bot: the bot to check the server name for
        :return: the server name
        """
        # Unnecessary
        return ""

    def get_channel(self, bot: str) -> str:
        """
        Checks to which channel a given xdcc-serving bot belongs to

        :param bot: the bot to check the channel name for
        :return: the channel name
        """
        # Unnecessary
        return ""
