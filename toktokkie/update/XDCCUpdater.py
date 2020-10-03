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

from typing import List, Dict, Any, Optional, Set
from puffotter.prompt import prompt
from xdcc_dl.xdcc import download_packs
from xdcc_dl.pack_search.SearchEngine import SearchEngineType, SearchEngine
from xdcc_dl.entities.XDCCPack import XDCCPack
from toktokkie.metadata.Metadata import Metadata
from toktokkie.update.TvUpdater import TvUpdater, DownloadInstructions


class XDCCUpdater(TvUpdater):
    """
    Class that handles the configuration and execution of an xdcc update
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the Updater
        """
        return "xdcc"

    @classmethod
    def search_engine_names(cls) -> Set[str]:
        """
        :return: The names of applicable search engines
        """
        return SearchEngineType.choices()

    @classmethod
    def json_schema(cls) -> Optional[Dict[str, Any]]:
        """
        :return: Optional JSON schema for a configuration file
        """
        schema = super().json_schema()
        schema["properties"]["bot"] = {"type": "string"}
        schema["required"].append("bot")
        return schema

    @property
    def search_engine(self) -> SearchEngine:
        """
        :return: The search engine to use
        """
        return SearchEngineType.resolve(self.config["search_engine"])

    @classmethod
    def predefined_patterns(cls) -> Dict[str, str]:
        """
        :return: Predefined search patterns for this updater
        """
        return {
            "horriblesubs": "[HorribleSubs] @{NAME} - @{EPI-2} [@{RES-P}].mkv"
        }

    def perform_search(self, search_term: str, search_regex: str) -> List[Any]:
        """
        Performs a search using the selected search engine
        :param search_term: The term to search for
        :param search_regex: The expected regex
        :return: The search results
        """
        search_results = super().perform_search(search_term, search_regex)
        search_results = [
            x for x in search_results if x.bot == self.bot
        ]
        return search_results

    @property
    def bot(self) -> str:
        """
        :return: The bot to use for updating
        """
        return self.config["bot"]

    @classmethod
    def _prompt(cls, metadata: Metadata) -> Optional[Dict[str, Any]]:
        """
        Prompts the user for information to create a config file
        :param metadata: The metadata of the media for which to create an
                         updater config file
        :return: The configuration JSON data
        """
        json_data = super()._prompt(metadata)
        json_data["bot"] = prompt("Bot", default="CR-HOLLAND|NEW")
        return json_data

    def download(self, download_instructions: List[DownloadInstructions]):
        """
        Performs a download
        :param download_instructions: The download instrcutions
        :return: None
        """
        packs = []
        for instructions in download_instructions:
            pack: XDCCPack = instructions.search_result
            pack.set_directory(instructions.directory)
            pack.set_filename(instructions.filename, True)
            pack.set_original_filename(
                pack.original_filename.replace("'", "_")
            )  # Fixes filenames
            packs.append(pack)

        download_packs(
            packs,
            timeout=self.args["timeout"],
            throttle=self.args["throttle"]
        )
