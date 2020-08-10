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
import json
import argparse
import requests
from typing import List, Dict
from toktokkie.Directory import Directory
from puffotter.graphql import GraphQlClient
from puffotter.os import makedirs, replace_illegal_ntfs_chars
from puffotter.prompt import prompt
from subprocess import Popen
from toktokkie.metadata.types.Manga import Manga
from toktokkie.exceptions import MissingMetadata, InvalidMetadata
from toktokkie.scripts.Command import Command


class MangaCreateCommand(Command):
    """
    Class that encapsulates behaviour of the manga-create command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "manga-create"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        parser.add_argument("urls", nargs="+",
                            help="The anilist or mangadex URLS of the manga "
                                 "series to create")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        titles = []  # type: List[str]
        ids = []

        for url in self.args.urls:
            urlparts = [x for x in url.split("/") if x]
            media_id = [x for x in urlparts if x.isdigit()][-1]
            for site in ["anilist", "mangadex"]:
                if urlparts[1].startswith(site):
                    ids.append((site, media_id))

        for site, media_id in ids:

            if site == "anilist":
                info = self.load_anilist_info(media_id)
            elif site == "mangadex":
                info = self.load_mangadex_info(media_id)
            else:
                continue

            titles.append(info["title"])
            self.prepare_directory(info["title"], info["cover"])

            title_ids = {
                "mangadex": [info["mangadex_id"]]
            }
            if info["anilist_id"] is not None:
                title_ids["anilist"] = [info["anilist_id"]]

            metadata = Manga(info["title"], {
                "ids": title_ids,
                "special_chapters": [],
                "type": "manga"
            })
            metadata.write()

        update_cmd = "toktokkie update "
        for title in titles:
            update_cmd += "\"{}\" ".format(title)

        print(update_cmd)

    def load_anilist_info(
            self, anilist_id: str, prompt_for_mangadex: bool = True
    ) -> Dict[str, str]:
        client = GraphQlClient("https://graphql.anilist.co")
        query = """
            query ($id: Int) {
                Media (id: $id) {
                    title {
                        romaji
                        english
                    }
                    coverImage {
                        large
                        medium
                    }
                }
            }
        """
        data = client.query(query, {"id": anilist_id})["data"]

        title = data["Media"]["title"]["english"]
        if title is None:
            title = data["Media"]["title"]["romaji"]
        title = replace_illegal_ntfs_chars(title)

        cover_image = data["Media"]["coverImage"]["large"]
        cover_image = cover_image.replace("medium", "large")
        mangadex_id = self.get_ids(anilist_id, "anilist").get("mangadex")

        if mangadex_id is None and prompt_for_mangadex:
            anilist_url = "https://anilist.co/manga/" + str(anilist_id)
            mangadex_search = "https://mangadex.org/quick_search/" + title
            print("Title:" + title)
            print("Anilist URL:" + anilist_url)
            print(mangadex_search)

            mangadex_id = prompt("Mangadex ID/URL: ")
            if "https://mangadex.org/title/" in mangadex_id:
                mangadex_id = mangadex_id \
                    .split("https://mangadex.org/title/")[1] \
                    .split("/")[0]

        return {
            "title": title,
            "cover": cover_image,
            "mangadex_id": mangadex_id,
            "anilist_id": anilist_id
        }

    def load_mangadex_info(self, mangadex_id: str) -> Dict[str, str]:
        url = "https://mangadex.org/api/manga/" + mangadex_id
        data = json.loads(requests.get(url).text)

        anilist_id = data["manga"]["links"].get("al")
        if anilist_id is not None:
            info = self.load_anilist_info(anilist_id, False)
            info["mangadex_id"] = mangadex_id
        else:
            info = {
                "title": data["manga"]["title"],
                "cover": "https://mangadex.org" + data["manga"]["cover_url"],
                "mangadex_id": mangadex_id,
                "anilist_id": anilist_id
            }

        return info

    # noinspection PyMethodMayBeStatic
    def get_ids(self, media_id: str, media_site: str) -> Dict[str, str]:
        url = f"https://dev.otaku-info.eu/api/v1/media_ids/" \
              f"{media_site}/manga/{media_id}"
        data = json.loads(requests.get(url).text)
        return data["data"]

    # noinspection PyMethodMayBeStatic
    def prepare_directory(self, title: str, cover_url: str):
        makedirs(title)
        makedirs(os.path.join(title, "Main"))
        makedirs(os.path.join(title, ".meta/icons"))

        try:
            Directory(title)
        except (MissingMetadata, InvalidMetadata):

            main_icon = os.path.join(title, ".meta/icons/main.")
            ext = cover_url.rsplit(".", 1)[1]

            img = requests.get(
                cover_url, headers={"User-Agent": "Mozilla/5.0"}
            )
            if img.status_code >= 300:
                med_url = cover_url.replace("large", "medium")
                img = requests.get(
                    med_url, headers={"User-Agent": "Mozilla/5.0"}
                )
            with open(main_icon + ext, "wb") as f:
                f.write(img.content)

            if ext != "png":
                Popen(["convert", main_icon + ext, main_icon + "png"]) \
                    .wait()
                os.remove(main_icon + ext)
            Popen([
                "zip", "-j",
                os.path.join(title, "cover.cbz"),
                main_icon + "png"
            ]).wait()
