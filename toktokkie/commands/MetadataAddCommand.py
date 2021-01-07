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
import argparse
from puffotter.os import makedirs
from toktokkie.commands.Command import Command
from toktokkie.enums import IdType
from toktokkie.enums import MediaType
from toktokkie.Directory import Directory
from toktokkie.exceptions import InvalidMetadata, MissingMetadata
from toktokkie.metadata.tv.Tv import Tv
from toktokkie.metadata.tv.components.TvSeason import TvSeason


class MetadataAddCommand(Command):
    """
    Class that encapsulates behaviour of the metadata-add command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "metadata-add"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        parser.add_argument("directory",
                            help="The directory to which to add metadata")

        subparser = parser.add_subparsers(dest="mode")

        tv_series_ids = [x.value for x in Tv.valid_id_types()]

        multi_episode_parser = subparser.add_parser(
            "multi-episode", help="Add a multi-episode to a TV Series"
        )
        multi_episode_parser.add_argument("id_type", choices=tv_series_ids,
                                          help="The ID type")
        multi_episode_parser.add_argument("season", type=int,
                                          help="The season of the episode")
        multi_episode_parser.add_argument("start_episode", type=int,
                                          help="The start episode")
        multi_episode_parser.add_argument("end_episode", type=int,
                                          help="The end episode")

        exclude_parser = subparser.add_parser(
            "exclude", help="Add an excluded episode to a TV Series"
        )
        exclude_parser.add_argument("id_type", choices=tv_series_ids,
                                    help="The ID type")
        exclude_parser.add_argument("season", type=int,
                                    help="The season of the episode")
        exclude_parser.add_argument("episode", type=int,
                                    help="The episode to exclude")

        season_parser = subparser.add_parser(
            "season", help="Adds a season to a TV Series"
        )
        season_parser.add_argument("season_name",
                                   help="The name of the season")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        try:
            directory = Directory(self.args.directory)
        except (MissingMetadata, InvalidMetadata):
            self.logger.warning(f"Invalid directory {self.args.directory}")
            return

        if directory.metadata.media_type() == MediaType.TV_SERIES:
            if self.args.mode == "multi-episode":
                self.add_multi_episode()
            elif self.args.mode == "exclude":
                self.add_exclude()
            elif self.args.mode == "season":
                self.add_season()
            else:  # pragma: no cover
                self.logger.error("Invalid command")
        else:
            self.logger.warning(f"Invalid directory for action "
                                f"{self.args.mode}")

    def add_multi_episode(self):
        """
        Adds a multi-episode to a tv series metadata
        :return: None
        """
        meta = Tv(self.args.directory)
        meta.add_multi_episode(
            IdType(self.args.id_type),
            self.args.season,
            self.args.start_episode,
            self.args.end_episode
        )
        meta.write()

    def add_exclude(self):
        """
        Adds an excluded episode to a tv series metadata
        :return: None
        """
        meta = Tv(self.args.directory)
        meta.add_exclude(
            IdType(self.args.id_type),
            self.args.season,
            self.args.episode
        )
        meta.write()

    def add_season(self):
        """
        Adds a season to a TV series metadata
        :return: None
        """
        meta = Tv(self.args.directory)
        season_name = self.args.season_name

        seasons = meta.seasons
        season_names = {x.name for x in meta.seasons}
        if season_name in season_names:
            self.logger.warning("Season already exists")
            return

        season_path = os.path.join(meta.directory_path, season_name)

        print(f"Enter IDs for season {season_name}")
        season_ids = meta.objectify_ids(meta.prompt_component_ids(
            meta.valid_id_types(),
            meta.stringify_ids(meta.ids),
            meta.create_id_fetcher(meta.directory_path)
        ))
        season = TvSeason(
            meta.directory_path,
            meta.ids,
            season_ids,
            season_name
        )
        seasons.append(season)
        meta.seasons = seasons
        makedirs(season_path)
        meta.write()
