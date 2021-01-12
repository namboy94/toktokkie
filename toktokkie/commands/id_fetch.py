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

import argparse
from typing import List, Dict
from toktokkie.enums import MediaType, IdType
from toktokkie.commands.Command import Command
from toktokkie.Directory import Directory
from toktokkie.utils.IdFetcher import IdFetcher
from toktokkie.metadata.tv.Tv import Tv


class IdFetchCommand(Command):
    """
    Class that encapsulates behaviour of the id-fetch command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "id-fetch"

    @classmethod
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Fills out IDs based on existing IDs"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        for directory in Directory.load_directories(self.args.directories):
            metadata = directory.metadata
            fetcher = IdFetcher(metadata.name, metadata.media_type())
            ids = metadata.ids

            self.logger.info(f"Fetching IDs for {metadata.name}")

            if metadata.media_type() == MediaType.TV_SERIES:
                self.fetch_season_ids(metadata, fetcher)
            # TODO implement ID fetching for all components
            # elif metadata.media_type() == MediaType.MUSIC_ARTIST:
            #     self.fetch_theme_song_ids()
            #     self.fetch_album_ids()
            # elif metadata.media_type() == MediaType.BOOK_SERIES:
            #     self.fetch_volume_ids()

            self.fill_ids(ids, metadata.valid_id_types(), fetcher)
            metadata.ids = ids
            metadata.write()

    def fetch_season_ids(self, metadata: Tv, fetcher: IdFetcher):
        """
        Fetches season IDs for a Tv metadata
        :param metadata: The Tv metadata
        :param fetcher: The ID fetcher to use
        :return: None
        """
        new_seasons = []
        for season in metadata.seasons:
            season_ids = season.ids
            self.fill_ids(season_ids, metadata.valid_id_types(), fetcher)
            season.ids = season_ids
            new_seasons.append(season)
        metadata.seasons = new_seasons
        metadata.write()

    def fill_ids(
            self,
            ids: Dict[IdType, List[str]],
            valid_id_types: List[IdType],
            fetcher: IdFetcher
    ):
        """
        Fills IDs using an ID Fetcher
        :param ids: The IDs to fill
        :param valid_id_types: List of valid ID types
        :param fetcher: The IdFetcher object to use
        :return: None
        """
        for id_type in valid_id_types:
            if len(ids[id_type]) == 0:
                results = fetcher.fetch_ids(id_type, ids)
                if results is not None:
                    ids[id_type] = results
                    self.logger.info(f"Found {id_type.value} ids: "
                                     f"{results}")
