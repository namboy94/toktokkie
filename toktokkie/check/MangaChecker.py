"""
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
"""

import os
import json
import requests
from typing import Optional
from toktokkie.check.Checker import Checker
from toktokkie.metadata.Manga import Manga
from toktokkie.metadata.components.enums import MangaIdType
from anime_list_apis.api.AnilistApi import AnilistApi


class MangaChecker(Checker):
    """
    Class that check Manga media for consistency
    """

    def check(self) -> bool:
        """
        Performs sanity checks and prints out anything that's wrong
        :return: The result of the check
        """
        valid = super().check()
        if self.config.get("anilist_user") is not None:
            valid = self._check_chapter_progress() and valid
        return valid

    def _check_icons(self) -> bool:
        """
        Only checks for a main.png icon file.
        :return: The result of the check
        """
        valid = True

        if not os.path.isdir(self.metadata.icon_directory):
            valid = self.error("Missing icon directory")

        main_icon = os.path.join(self.metadata.icon_directory, "main.png")
        if not os.path.isfile(main_icon):
            valid = self.error("Missing main icon file for {}".format(
                self.metadata.name
            ))

        return valid

    def _check_chapter_progress(self) -> bool:
        """
        Checks the chapter progress using the best guess anilist user data
        can give us.
        :return: The result of the check
        """
        # noinspection PyTypeChecker
        metadata = self.metadata  # type: Manga

        local_chaptercount = len(os.listdir(metadata.main_path))

        try:
            anilist_id = int(metadata.ids.get(MangaIdType.ANILIST)[0])
            remote_chaptercount = self._guess_latest_chapter(int(anilist_id))
            if remote_chaptercount is None:
                return True
            else:
                complete = remote_chaptercount == local_chaptercount
                if not complete:
                    self.warn("Local chapters and available chapters "
                              "don't match: Local: {} / Available: {}"
                              .format(local_chaptercount, remote_chaptercount))
                return complete
        except (IndexError, ValueError):
            return True

    def _guess_latest_chapter(self, anilist_id: int) -> Optional[int]:
        """
        Guesses the latest chapter number based on anilist user activity
        :param anilist_id: The anilist ID to check
        :return: The latest chapter number
        """
        api = self.config["anilist_api"]  # type: AnilistApi
        info = api.get_manga_data(anilist_id)

        chapter_count = info.chapter_count
        if chapter_count is None:
            query = """
            query ($id: Int) {
              Page(page: 1) {
                activities(mediaId: $id, sort: ID_DESC) {
                  ... on ListActivity {
                    progress
                    userId
                  }
                }
              }
            }
            """
            resp = requests.post(
                "https://graphql.anilist.co",
                json={"query": query, "variables": {"id": anilist_id}}
            )
            data = json.loads(resp.text)["data"]["Page"]["activities"]

            progresses = []
            for entry in data:
                progress = entry["progress"]
                if progress is not None:
                    progress = entry["progress"].split(" - ")[-1]
                    progresses.append(progress)

            progresses.sort()

            best_guess = progresses.pop(-1)
            while progresses.count(best_guess) < 1:
                best_guess = progresses.pop(-1)

            chapter_count = best_guess

        print(chapter_count)
        return chapter_count
