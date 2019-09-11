#!/usr/bin/env python

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


import json
import argparse
import requests
from colorama import Fore, Style


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("anilist_username")
    parser.add_argument("custom_list", default=None)
    args = parser.parse_args()

    query = """
    query ($username: String) {
        MediaListCollection(userName: $username, type: MANGA) {
            lists {
                name
                entries {
                    status
                    progress
                    progressVolumes
                    media {
                        id
                        status
                        chapters
                        volumes
                        title {
                            english
                            romaji
                        }
                    }
                }
            }
        }
    }
    """
    user_lists = json.loads(requests.post(
        "https://graphql.anilist.co",
        json={"query": query, "variables": {"username": args.anilist_username}}
    ).text)["data"]["MediaListCollection"]["lists"]
    entries = []
    for _list in user_lists:
        if args.custom_list is None or _list["name"] == args.custom_list:
            entries += _list["entries"]

    for entry in entries:
        name = entry["media"]["title"]["english"]
        if name is None:
            name = entry["media"]["title"]["romaji"]

        user_progress = entry["progress"]
        list_chapters = entry["media"]["chapters"]
        if list_chapters is None:
            list_chapters = guess_latest_chapter(entry["media"]["id"])

        if user_progress != list_chapters:
            print(Fore.LIGHTRED_EX, end="")

        print("{}: ({}/{})".format(name, user_progress, list_chapters))
        print(Style.RESET_ALL, end="")


def guess_latest_chapter(anilist_id: int) -> int:
    """
    Guesses the latest chapter number based on anilist user activity
    :param anilist_id: The anilist ID to check
    :return: The latest chapter number
    """
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
            progresses.append(int(progress))

    progresses.sort()
    return progresses[-1]


if __name__ == "__main__":
    main()
