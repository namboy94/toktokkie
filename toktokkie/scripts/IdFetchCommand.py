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

import tvdb_api
import argparse
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.scripts.Command import Command
from toktokkie.Directory import Directory


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
        tvdb = tvdb_api.Tvdb()

        for directory in Directory.load_directories(self.args.directories):
            metadata = directory.metadata
            ids = metadata.ids

            self.logger.info(f"Fetching IDs for {metadata.name}")

            tvdb_ids = ids[IdType.TVDB]
            imdb_ids = ids[IdType.IMDB]

            if len(tvdb_ids) > 0 and len(imdb_ids) == 0:
                for tvdb_id in tvdb_ids:
                    self.logger.debug(f"Loading IMDB ID for {tvdb_id}")
                    imdb_id = tvdb[int(tvdb_id)].data["imdbId"]
                    if imdb_id:
                        self.logger.info(f"Loaded imdb ID '{imdb_id}' "
                                         f"for TVDB ID '{tvdb_id}'")
                        imdb_ids.append(imdb_id)
                    else:
                        self.logger.warning(f"No IMDB ID for {tvdb_id}")

            ids.update({
                IdType.TVDB: tvdb_ids,
                IdType.IMDB: imdb_ids
            })

            metadata.ids = ids
            metadata.write()
