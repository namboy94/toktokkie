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
import re
from enum import Enum
from typing import List, Dict, Any, Optional, cast, Set
from puffotter.prompt import prompt
from toktokkie.update.Updater import Updater
from toktokkie.renaming.Renamer import Renamer
from toktokkie.renaming.RenameOperation import RenameOperation
from toktokkie.metadata.MediaType import MediaType
from toktokkie.metadata.types.TvSeries import TvSeries
from toktokkie.metadata.Metadata import Metadata
from toktokkie.metadata.types.components.TvSeason import TvSeason
from toktokkie.exceptions import InvalidUpdateInstructions


class DownloadInstructions:
    """
    The instructions for a download
    """

    def __init__(self, search_result: Any, directory: str, filename: str):
        """
        Initializes the download instructions
        :param search_result: The search result object
        :param directory: The directory in which to download to
        :param filename: The filename to which to download to
        """
        self.search_result = search_result
        self.directory = directory
        self.filename = filename


class Resolution(Enum):
    """
    Enum that models the different resolution options
    """
    X1080p = "1080p"
    X720p = "720p"
    X480p = "480p"


# noinspection PyAbstractClass
class TvUpdater(Updater):
    """
    Class that handles the configuration and execution of a generic tv updater
    """

    @classmethod
    def applicable_media_types(cls) -> List[MediaType]:
        """
        :return: A list of media type with which the updater can be used with
        """
        return [MediaType.TV_SERIES]

    @classmethod
    def search_engine_names(cls) -> Set[str]:
        """
        :return: The names of applicable search engines
        """
        raise NotImplementedError()

    @classmethod
    def predefined_patterns(cls) -> Dict[str, str]:
        """
        :return: Predefined search patterns for this updater
        """
        raise NotImplementedError()

    @property
    def search_engine(self) -> Any:
        """
        :return: The search engine to use
        """
        raise NotImplementedError()

    def download(self, download_instructions: List[DownloadInstructions]):
        """
        Performs a download
        :param download_instructions: The download instrcutions
        :return: None
        """
        raise NotImplementedError()

    @classmethod
    def json_schema(cls) -> Optional[Dict[str, Any]]:
        """
        :return: Optional JSON schema for a configuration file
        """
        search_engine_pattern = "^({})$".format(
            "|".join(cls.search_engine_names())
        )
        resolution_pattern = \
            "^({})$".format("|".join([x.value for x in Resolution]))

        return {
            "type": "object",
            "properties": {
                "season": {"type": "string"},
                "search_name": {"type": "string"},
                "search_engine": {
                    "type": "string",
                    "pattern": search_engine_pattern
                },
                "resolution": {
                    "type": "string",
                    "pattern": resolution_pattern
                },
                "episode_offset": {"type": "number"},
                "search_pattern": {"type": "string"}
            },
            "required": [
                "season",
                "search_name",
                "search_engine",
                "resolution",
                "search_pattern"
            ],
            "additionalProperties": False
        }

    @property
    def season(self) -> TvSeason:
        """
        :return: The season to update
        """
        season_name = self.config["season"]
        metadata = cast(TvSeries, self.metadata)
        for season in metadata.seasons:
            if season.name == season_name:
                return season
        raise InvalidUpdateInstructions(
            "Invalid Season {}".format(season_name)
        )

    @property
    def search_name(self) -> str:
        """
        :return: The name of the series for searching purposes
        """
        return self.config["search_name"]

    @property
    def resolution(self) -> Resolution:
        """
        :return: The resolution in which to update the series
        """
        return Resolution(self.config["resolution"])

    @property
    def p_resolution(self) -> str:
        """
        :return: The resolution in P-notation (1080p)
        """
        return self.resolution.value

    @property
    def x_resolution(self) -> str:
        """
        :return: The resolution in X-notation (1920x1080)
        """
        if self.resolution == Resolution.X1080p:
            return "1920x1080"
        elif self.resolution == Resolution.X720p:
            return "1280x720"
        else:  # self.resolution == Resolution.X480p
            return "720x480"

    @property
    def episode_offset(self) -> int:
        """
        :return: The amount of episodes offset from 1 when updating
        """
        return int(self.config["episode_offset"])

    @property
    def search_pattern(self) -> str:
        """
        :return: The search pattern to use
        """
        pattern = self.config["search_pattern"]
        return self.predefined_patterns().get(pattern, pattern)

    @classmethod
    def _prompt(cls, metadata: Metadata) -> Optional[Dict[str, Any]]:
        """
        Prompts the user for information to create a config file
        :param metadata: The metadata of the media for which to create an
                         updater config file
        :return: The configuration JSON data
        """
        metadata = cast(TvSeries, metadata)
        print(f"Generating {cls.name()} "
              f"Update instructions for {metadata.name}")

        normal_seasons = [
            x.name for x in metadata.seasons if x.name.startswith("Season ")
        ]

        default_season = None  # type: Optional[str]
        if len(normal_seasons) > 0:
            default_season = max(normal_seasons)

        json_data = {
            "season": prompt("Season", default=default_season),
            "search_name": prompt("Search Name", default=metadata.name),
            "search_engine": prompt(
                "Search Engine",
                choices=cls.search_engine_names()
            ),
            "resolution": prompt(
                "Resolution",
                default="1080p",
                choices={"1080p", "720p", "480p"}
            ),
            "episode_offset": prompt(
                "Episode Offset", default=0, _type=int
            )
        }

        print("-" * 80)
        print("Valid variables for search patterns:")

        for variable in [
            "@{NAME}",
            "@{RES-P}",
            "@{RES-X}",
            "@{HASH}",
            "@{EPI-1}",
            "@{EPI-2}",
            "@{EPI-3}",
            "@{ANY}"
        ]:
            print(variable)

        print("-" * 80)
        print("Predefined patterns:")

        for pattern_name, pattern in cls.predefined_patterns().items():
            print(f"{pattern_name} ({pattern})")

        print("-" * 80)
        json_data["search_pattern"] = prompt("Search Pattern")

        return json_data

    def perform_search(self, search_term: str, search_regex: str) -> List[Any]:
        """
        Performs a search using the selected search engine
        :param search_term: The term to search for
        :param search_regex: The expected regex
        :return: The search results
        """
        search_results = self.search_engine.search(search_term)

        search_regex = re.compile(search_regex)
        search_results = list(filter(
            lambda x: re.match(search_regex, x.filename),
            search_results
        ))
        return search_results

    def update(self):
        """
        Executes the XDCC Update procedure
        :return: None
        """
        self._update_episode_names()

        start_episode = 1 + len(os.listdir(self.season.path))
        start_episode += self.episode_offset

        episode_count = start_episode
        download_instructions = []

        while True:
            search_term = self._generate_search_term(episode_count, False)
            search_regex = self._generate_search_term(episode_count, True)
            search_results = self.perform_search(search_term, search_regex)

            if len(search_results) > 0:
                result = search_results[0]

                try:
                    ext = "." + result.filename.rsplit(".")[1]
                except IndexError:
                    ext = ""

                episode_number = episode_count - self.episode_offset
                episode_name = "{} - S{}E{} - Episode {}{}".format(
                    self.metadata.name,
                    str(self.season.season_number).zfill(2),
                    str(episode_number).zfill(2),
                    episode_number,
                    ext
                )
                episode_name = RenameOperation.sanitize(
                    self.season.path, episode_name
                )

                download_instructions.append(DownloadInstructions(
                    result, self.season.path, episode_name
                ))
                episode_count += 1

            else:
                break

        self.download(download_instructions)
        self._update_episode_names()

    def validate(self):
        """
        Checks if the configuration is valid
        :return: None
        """
        super().validate()

        # Check is done in season property definition
        self.logger.debug("Loading season {}".format(self.season))

    def _update_episode_names(self):
        """
        Renames the episodes in the season directory that's being updated
        :return: None
        """
        renamer = Renamer(self.metadata)
        for operation in renamer.operations:
            operation_dir = os.path.basename(os.path.dirname(operation.source))
            if operation_dir == self.season.name:
                operation.rename()

    def _generate_search_term(self, episode: int, regex: bool) -> str:
        """
        Generates a search term/search term regex for a specified episode
        :param episode: The episode for which to generate the search term
        :param regex: Whether or not to generate a regex.
        :return: The generated search term/regex
        """
        pattern = self.search_pattern
        pattern = pattern.replace("@{NAME}", self.search_name)
        pattern = pattern.replace("@{RES-P}", self.p_resolution)
        pattern = pattern.replace("@{RES-X}", self.x_resolution)

        if regex:
            pattern = pattern.replace("[", "\\[")
            pattern = pattern.replace("]", "\\]")
            pattern = pattern.replace("(", "\\(")
            pattern = pattern.replace(")", "\\)")
            pattern = pattern.replace("@{HASH}", "[a-zA-Z0-9]+")
            pattern = pattern.replace(
                "@{EPI-1}", str(episode).zfill(1) + "(v[0-9]+)?"
            )
            pattern = pattern.replace(
                "@{EPI-2}", str(episode).zfill(2) + "(v[0-9]+)?"
            )
            pattern = pattern.replace(
                "@{EPI-3}", str(episode).zfill(3) + "(v[0-9]+)?"
            )
            pattern = pattern.replace("@{ANY}", ".*?")

        else:
            pattern = pattern.replace("@{EPI-1}", str(episode).zfill(1))
            pattern = pattern.replace("@{EPI-2}", str(episode).zfill(2))
            pattern = pattern.replace("@{EPI-3}", str(episode).zfill(3))
            pattern = pattern.replace("[@{HASH}]", "")
            pattern = pattern.replace("@{HASH}", "")
            pattern = pattern.replace("@{ANY}", "")

        return pattern
