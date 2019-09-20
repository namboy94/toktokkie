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
from colorama import Fore, Style
from toktokkie.metadata.Manga import Manga
from toktokkie.metadata.components.enums import MediaType, MangaIdType
from manga_dl.scrapers.mangadex import MangaDexScraper
from puffotter.os import makedirs
from toktokkie.scripts.Command import Command


class MangaUpdateCommand(Command):
    """
    Class that encapsulates behaviour of the manga-update command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "manga-update"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)
        parser.add_argument("--dry-run", action="store_true",
                            help="Does not download or rename anything")

    def execute(self, args: argparse.Namespace):
        """
        Executes the commands
        :param args: The command line arguments
        :return: None
        """
        scraper = MangaDexScraper()

        for directory in self.load_directories(
                args.directories, [MediaType.MANGA]
        ):
            print(directory.metadata.name)

            metadata = directory.metadata  # type: Manga

            mangadex_id = metadata.ids.get(MangaIdType.MANGADEX)
            if mangadex_id is None or len(mangadex_id) == 0:
                print("No mangadex ID for {}".format(directory.path))
                continue

            chapters = scraper.load_chapters(None, mangadex_id[0])
            main_chapters = []
            special_chapters = []

            for chapter in chapters:
                if "." in chapter.chapter_number:
                    special_chapters.append(chapter)
                else:
                    try:
                        int(chapter.chapter_number)
                        main_chapters.append(chapter)
                    except ValueError:
                        special_chapters.append(chapter)

            current_latest = len(os.listdir(metadata.main_path))
            main_chapters = list(filter(
                lambda x: int(x.chapter_number) > current_latest,
                main_chapters
            ))

            if not args.dry_run:
                directory.rename(noconfirm=True)
            maxchar = max(metadata.name)

            total_chapters = len(main_chapters) + current_latest

            downloaded = []
            for c in main_chapters:
                if current_latest + 1 != c.macro_chapter:
                    print("{}Missing chapter {}, expected {}{}".format(
                        Fore.LIGHTRED_EX,
                        current_latest + 1,
                        c.chapter_number,
                        Style.RESET_ALL
                    ))
                    break
                current_latest += 1

                if c.chapter_number in downloaded:
                    continue
                downloaded.append(c.chapter_number)

                name = "{}{} - Chapter {}.cbz".format(
                    maxchar,
                    metadata.name,
                    c.chapter_number.zfill(len(str(total_chapters)))
                )
                dest = os.path.join(metadata.main_path, name)
                if not args.dry_run:
                    print("Downloading Chapter {}".format(c))
                    c.download(dest)
                else:
                    print("{}Found chapter: {}{}".format(
                        Fore.LIGHTYELLOW_EX,
                        c,
                        Style.RESET_ALL
                    ))

            if not args.dry_run:
                directory.rename(noconfirm=True)

            for c in special_chapters:

                if c.chapter_number not in metadata.special_chapters:
                    scraper.logger.info("Found unknown chapter {}"
                                        .format(c.chapter_number))
                    continue

                else:
                    path = os.path.join(
                        metadata.special_path,
                        "{} - Chapter {}.cbz"
                        .format(metadata.name, c.chapter_number)
                    )
                    if os.path.exists(path):
                        continue
                    else:
                        if not args.dry_run:
                            makedirs(metadata.special_path)
                            c.download(path)
                        else:
                            print("{}Found chapter: {}{}".format(
                                Fore.LIGHTYELLOW_EX,
                                c,
                                Style.RESET_ALL
                            ))
