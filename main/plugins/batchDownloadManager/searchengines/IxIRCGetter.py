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

import requests
from bs4 import BeautifulSoup

from plugins.batchDownloadManager.searchengines.GenericGetter import GenericGetter
from plugins.batchDownloadManager.searchengines.objects.XDCCPack import XDCCPack


class IxIRCGetter(GenericGetter):
    """
    Class that gets xdcc packlists from ixirc.com
    """

    def search(self):
        """
        Conducts the search
        :return: the search results as a list of XDCCPack objects
        """
        split_search_term = self.search_term.split(" ")
        prepared_search_term = split_search_term[0]
        i = 1
        while i < len(split_search_term):
            prepared_search_term += "+" + split_search_term[i]
            i += 1

        number_of_pages = 1

        base_url = "https://ixirc.com/?q=" + prepared_search_term
        content = BeautifulSoup(requests.get(base_url).text, "html.parser")
        page_analysis = content.select("h3")

        if "Over" in page_analysis[0].text:
            number_of_pages = 2

        analysing = False
        if number_of_pages == 2:
            analysing = True
        while analysing:
            url = "https://ixirc.com/?q=" + prepared_search_term + "&pn=" + str(number_of_pages - 1)
            content = BeautifulSoup(requests.get(url).text, "html.parser")
            page_analysis = content.select("h3")
            if "Over" in page_analysis[0].text:
                number_of_pages += 1
                continue
            else:
                analysing = False

        i = 1
        urls = [base_url]
        while i < number_of_pages:
            urls.append("https://ixirc.com/?q=" + prepared_search_term + "&pn=" + str(i))
            i += 1

        results = []

        for url in urls:
            content = BeautifulSoup(requests.get(url).text, "html.parser")
            packs = content.select("td")
            self.__getPageResults__(packs, results)

        return results

    @staticmethod
    def __getPageResults__(packs, results):
        """
        Gets the page results?
        I apologize for this docstring
        :param packs: the packs
        :param results: the results
        :return: void
        """
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

    def get_server(self, bot):
        """
        Not needed due to how this getter is designed
        :param bot: the bot to check
        :return: void
        """
        print()

    def get_channel(self, bot):
        """
        Not needed due to how this getter is designed
        :param bot: the bot to check
        :return: void
        """
        print()
