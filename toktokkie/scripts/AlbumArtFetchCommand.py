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
import requests
import argparse
from PIL import Image
from toktokkie.scripts.Command import Command
from toktokkie.metadata.ids.IdType import IdType
from toktokkie.metadata.MediaType import MediaType
from puffotter.graphql import GraphQlClient


class AlbumArtFetchCommand(Command):
    """
    Class that encapsulates behaviour of the album-art-fetch command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "album-art-fetch"

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
        client = GraphQlClient("https://graphql.anilist.co")

        query = """
            query ($id: Int) {
                Media (id: $id) {
                    coverImage {
                        large
                    }
                }
            }
        """

        for directory in self.load_directories(
                self.args.directories, restrictions=[MediaType.MUSIC_ARTIST]
        ):
            for album in directory.metadata.theme_songs:

                self.logger.info("Fetching cover art for {}"
                                 .format(album["name"]))

                anilist_id = album["series_ids"].get(IdType.ANILIST)
                if anilist_id is None:
                    self.logger.warning("{} has no anilist ID, skipping"
                                        .format(album["name"]))
                    continue

                album_icon_file = os.path.join(
                    directory.metadata.icon_directory,
                    album["name"] + ".png"
                )
                tmp_file = "/tmp/coverimage-temp"

                data = client.query(query, {"id": int(anilist_id[0])})["data"]
                cover_image = data["Media"]["coverImage"]["large"]
                cover_image = cover_image.replace("medium", "large")
                img = requests.get(
                    cover_image, headers={"User-Agent": "Mozilla/5.0"}
                )
                if img.status_code >= 300:
                    med_url = cover_image.replace("large", "medium")
                    img = requests.get(
                        med_url, headers={"User-Agent": "Mozilla/5.0"}
                    )
                with open(tmp_file, "wb") as f:
                    f.write(img.content)

                image = Image.open(tmp_file)
                x, y = image.size
                new_y = 512
                new_x = int(new_y * x / y)

                image = image.resize((new_x, new_y), Image.ANTIALIAS)

                x, y = image.size
                size = 512

                new = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
                new.paste(image, (int((size - x) / 2), int((size - y) / 2)))

                with open(album_icon_file, "wb") as f:
                    new.save(f)
