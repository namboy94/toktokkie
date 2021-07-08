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
from bs4 import BeautifulSoup
from typing import Dict, List
from toktokkie.Directory import Directory
from toktokkie.commands.Command import Command
from toktokkie.enums import IdType
from toktokkie.enums import MediaType
from toktokkie.metadata.music.Music import Music
from toktokkie.metadata.music.components.MusicThemeSong import MusicThemeSong
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
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Loads music album art based on stored IDs"

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
        for directory in Directory.load_directories(
                self.args.directories, restrictions=[MediaType.MUSIC_ARTIST]
        ):
            metadata = directory.metadata  # type: Music
            theme_songs = {
                x.name: x for x in metadata.theme_songs
            }  # type: Dict[str, MusicThemeSong]
            for album in metadata.albums:

                theme_song = theme_songs.get(album.name)

                self.logger.info("Fetching cover art for {}"
                                 .format(album.name))

                album_icon_file = os.path.join(
                    metadata.icon_directory,
                    album.name + ".png"
                )

                if os.path.isfile(album_icon_file):
                    self.logger.info("Album art already exists, skipping")
                    continue

                musicbrainz_ids = album.ids[IdType.MUSICBRAINZ_RELEASE]
                youtube_ids = album.ids[IdType.YOUTUBE_VIDEO]

                if len(musicbrainz_ids) >= 1:
                    self.logger.debug("Using musicbrainz IDs")
                    cover_urls = self.load_musicbrainz_cover_url(
                        musicbrainz_ids[0]
                    )
                elif theme_song is not None:
                    self.logger.debug("Using anilist IDs")
                    anilist_ids = theme_song.series_ids[IdType.ANILIST]
                    if len(anilist_ids) < 1:
                        self.logger.warning("{} has no anilist ID, skipping"
                                            .format(theme_song.name))
                        continue

                    cover_urls = self.load_anilist_cover_url(anilist_ids[0])
                elif len(youtube_ids) >= 1:
                    self.logger.debug("Using musicbrainz IDs")
                    cover_urls = self.load_youtube_cover_urls(
                        youtube_ids
                    )
                else:
                    self.logger.warning("Couldn't find album art for {}"
                                        .format(album.name))
                    continue

                self.download_cover_file(cover_urls, album_icon_file)

    def download_cover_file(self, urls: List[str], dest: str):
        """
        Downloads a cover file, then trims it correctly and/or converts
        it to PNG
        :param urls: The URLs to try
        :param dest: The destination file location
        :return: None
        """
        tmp_file = "/tmp/coverimage-temp"

        img = None
        while len(urls) > 0:
            url = urls.pop(0)
            self.logger.info("Trying to download {}".format(url))
            img = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            if img.status_code < 300:
                break
            else:
                img = None

        if img is None:
            self.logger.warning("Couldn't download cover file {}".format(dest))
            return

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

        with open(dest, "wb") as f:
            new.save(f)

    # noinspection PyMethodMayBeStatic
    def load_musicbrainz_cover_url(self, musicbrainz_id: str) -> List[str]:
        """
        Loads cover image URls using musicbrainz release IDs
        :param musicbrainz_id: The musicbrainz release ID to use
        :return: The musicbrainz cover image URLs
        """
        cover_page_url = "https://musicbrainz.org/release/{}/cover-art"\
            .format(musicbrainz_id)

        cover_page = BeautifulSoup(
            requests.get(cover_page_url).text,
            "html.parser"
        )

        urls = []
        urlmap = {
            "original": [],
            "250px": [],
            "500px": []
        }  # type: Dict[str, List[str]]

        for art in cover_page.select(".artwork-cont"):
            for a in art.find_all("a"):
                category = a.text.strip().lower()
                if category in ["original", "250px", "500px"]:
                    urlmap[category].append(a["href"])

        for category in ["original", "500px", "250px"]:
            for link in urlmap[category]:
                urls.append("https:" + link)

        try:
            displayed = cover_page.select(".cover-art")[0].find("img")["src"]
            if displayed.startswith("/"):
                displayed = "https:" + displayed
            urls.append(displayed)
        except (IndexError, TypeError):
            pass

        return urls

    # noinspection PyMethodMayBeStatic
    def load_anilist_cover_url(self, anilist_id: str) -> List[str]:
        """
        Loads cover image URLs using anilist IDs
        :param anilist_id: The anilist ID to use
        :return: The cover images that were found
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
        data = client.query(query, {"id": int(anilist_id)})["data"]
        cover_image = data["Media"]["coverImage"]["large"]

        return [
            cover_image.replace("medium", "large"),
            cover_image.replace("large", "medium"),
            cover_image.replace("large", "small").replace("medium", "small")
        ]

    def load_youtube_cover_urls(self, youtube_ids: List[str]) -> List[str]:
        return [
            f"https://i.ytimg.com/vi/{youtube_id}/maxresdefault.jpg"
            for youtube_id in youtube_ids
        ]
