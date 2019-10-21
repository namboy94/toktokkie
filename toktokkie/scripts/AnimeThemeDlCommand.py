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
import time
import shutil
import argparse
import musicbrainzngs
from anime_list_apis.api.AnilistApi import AnilistApi
from anime_list_apis.models.attributes.MediaType import MediaType
from typing import Tuple, Dict, List, Any
from bs4 import BeautifulSoup
from toktokkie import version
from toktokkie.scripts.Command import Command
from toktokkie.metadata.MusicArtist import MusicArtist
from puffotter.subprocess import execute_command
from puffotter.print import pprint
from puffotter.os import makedirs, listdir
from puffotter.requests import aggressive_request
from toktokkie.scripts.RenameCommand import RenameCommand
from toktokkie.scripts.PlaylistCreateCommand import PlaylistCreateCommand
from toktokkie.scripts.AlbumArtFetchCommand import AlbumArtFetchCommand
from toktokkie.scripts.MusicTagCommand import MusicTagCommand


class AnimeThemeDlCommand(Command):
    """
    Class that encapsulates behaviour of the anitheme-dl command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "anitheme-dl"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        parser.add_argument("year", type=int,
                            help="The year for which to download songs")
        parser.add_argument("season", type=str,
                            choices={"Spring", "Winter", "Summer", "Fall"},
                            help="The season for which to download songs.")
        parser.add_argument("--out", "-o", default="dl",
                            help="The destination directory")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        makedirs(self.args.out)
        for subdir in ["webm", "mp3", "covers"]:
            makedirs(os.path.join(self.args.out, subdir))

        series_names = self.load_titles(self.args.year, self.args.season)
        selected_series = self.prompt_selection(series_names)

        self.logger.info("Loading data...")
        selected_songs = self.load_data(
            self.args.year,
            self.args.season,
            selected_series
        )
        selected_songs = self.handle_excludes(selected_songs)

        self.logger.info("Downloading Openings")
        self.download_webms(selected_songs)
        self.logger.info("Converting to MP3")
        self.convert_to_mp3(selected_songs)

        self.logger.info("Generating Artist/Album Structure")
        self.generate_artist_album_structure(selected_songs)

        self.post_commands()

        self.logger.info("Done")

    def post_commands(self):
        """
        Commands executed after the core anitheme-dl functionality has
        been completed
        :return: None
        """
        structure_dir = os.path.join(self.args.out, "structured")
        ops_dir = os.path.join(structure_dir, "OP")
        eds_dir = os.path.join(structure_dir, "ED")

        for category in [ops_dir, eds_dir]:
            dirs = list(map(lambda x: x[1], listdir(category)))

            rename_ns = argparse.Namespace()
            rename_ns.__dict__["directories"] = dirs
            rename_ns.__dict__["noconfirm"] = True
            RenameCommand(rename_ns).execute()

            playlist_ns = argparse.Namespace()
            playlist_ns.__dict__["directories"] = dirs
            playlist_ns.__dict__["playlist_file"] = os.path.join(
                structure_dir,
                "{} playlist.m3u".format(os.path.basename(category))
            )
            playlist_ns.__dict__["format"] = "m3u"
            playlist_ns.__dict__["prefix"] = None
            PlaylistCreateCommand(playlist_ns).execute()

            album_art_ns = argparse.Namespace()
            album_art_ns.__dict__["directories"] = dirs
            AlbumArtFetchCommand(album_art_ns).execute()

            music_tag_ns = argparse.Namespace()
            music_tag_ns.__dict__["directories"] = dirs
            MusicTagCommand(music_tag_ns).execute()

    def load_titles(
            self,
            year: int,
            season: str,
            include_previous_season: bool = True
    ) -> List[str]:
        """
        Loads a list of titles which can then be selected by the user
        :param year: The year for which to fetch titles
        :param season: The season for which to fetch titles
        :param include_previous_season: Whether to include the previous season
        :return: The list of titles
        """
        url = "https://old.reddit.com/r/AnimeThemes/wiki/" \
              "{}#wiki_{}_{}_season".format(year, year, season)
        response = aggressive_request(url)

        soup = BeautifulSoup(response, "html.parser")
        listings = soup.find("div", {"class": "md wiki"})

        entries = listings.find_all("h3")
        entries = list(map(lambda x: x.text, entries))

        position = {"Winter": 1, "Spring": 2, "Summer": 3, "Fall": 4}
        segments = self.segmentize(entries)

        this_segment = segments[-position[season]]

        if include_previous_season:
            if season == "Winter":
                additional_segment = self.load_titles(year - 1, "Fall", False)
            else:
                additional_segment = segments[-position[season] + 1]
            return additional_segment + this_segment
        else:
            return this_segment

    @staticmethod
    def segmentize(titles: List[str]) -> List[List[str]]:
        """
        Segments a list of titles into segments
        :param titles: The titles to segmentize
        :return: The segments
        """

        segments = []
        current_segment = []

        for i, title in enumerate(titles):
            if i > 0 \
                    and titles[i - 1] > title \
                    and titles[i - 1][0].lower() != title[0].lower():
                segments.append(current_segment)
                current_segment = []
            current_segment.append(title)
        segments.append(current_segment)

        return segments

    def prompt_selection(self, shows: List[str]) -> List[str]:
        """
        Prompts the user for a selection of series for which to download songs
        :param shows: All series that are up for selection
        :return: A list of series names that were selected
        """
        selection_file = os.path.join(self.args.out, "selection.json")
        if os.path.isfile(selection_file):
            with open(selection_file, "r") as f:
                old_selection = json.loads(f.read())

            while True:
                resp = input("Use previous selection? {} (y|n)"
                             .format(old_selection))
                if resp.lower() in ["y", "n"]:
                    if resp.lower() == "y":
                        return old_selection
                    else:
                        break
                else:
                    continue

        segments = self.segmentize(shows)
        counter = 0
        for segment in segments:
            print("-" * 80)
            for show in segment:
                print("[{}]: {}".format(counter + 1, show))
                counter += 1

        while True:

            selection = input(
                "Please select the series for which to download songs: "
            ).strip()

            if selection == "":
                print("Invalid Selection")
                continue

            try:
                selection = selection.strip().split(",")
                selection = list(map(lambda x: shows[int(x) - 1], selection))
            except (ValueError, IndexError):
                print("Invalid Selection")
                continue

            with open(selection_file, "w") as f:
                f.write(json.dumps(selection))

            return selection

    def handle_excludes(
            self,
            selected_songs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Allows the user to exclude certain songs from being downloaded
        Deletes any  files that may already exist for excluded songs
        :param selected_songs: All currently selected songs
        :return: The selected songs minus any excluded songs
        """
        excludes_file = os.path.join(self.args.out, "excludes.json")

        use_old = False
        excludes = []

        if os.path.isfile(excludes_file):
            with open(excludes_file, "r") as f:
                old_selection = json.loads(f.read())

            while True:
                resp = input("Use previous exclusion? {} (y|n)"
                             .format(old_selection))
                if resp.lower() in ["y", "n"]:
                    if resp.lower() == "y":
                        excludes = old_selection
                        use_old = True
                    break

        if not use_old:
            for i, song in enumerate(selected_songs):
                print("[{}]: {} ({})"
                      .format(i + 1, song["filename"], song["song_info"][2]))

            while True:

                selection = \
                    input("Please select the songs to exclude: ").strip()

                if selection == "":
                    excludes = []
                    break
                try:
                    selection = selection.strip().split(",")
                    excludes = list(map(
                        lambda x: selected_songs[int(x) - 1]["filename"],
                        selection
                    ))
                except (ValueError, IndexError):
                    print("Invalid Selection")
                    continue
                break

        with open(excludes_file, "w") as f:
            f.write(json.dumps(excludes))

        new_selection = []
        for song in selected_songs:
            if song["filename"] not in excludes:
                new_selection.append(song)
            else:
                for _file in ["webm_file", "mp3_file", "cover_file"]:
                    if os.path.isfile(song[_file]):
                        pprint("Deleting {}".format(song[_file]), fg="magenta")
                        os.remove(song[_file])

        return new_selection

    def load_data(
            self,
            year: int,
            season: str,
            selected_series: List[str],
            include_previous_season: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Loads the Opening/Ending information from a combination of sources.
        :param year: The year to check
        :param season: The season to check
        :param selected_series: The series to consider
        :param include_previous_season: Whether to load data
                                        from previous seasons
        :return: The information in the following format:
                    [
                        {show, type, song, link, filename,
                        mp3_file, webm_file, cover_file,
                        mal_id, mal_title, mal_cover, mal_openings,
                        mal_endings, song_info}
                    ]
        """
        url = "https://old.reddit.com/r/AnimeThemes/wiki/" \
              "{}#wiki_{}_{}_season".format(year, year, season)
        response = aggressive_request(url)

        soup = BeautifulSoup(response, "html.parser")
        listings = soup.find("div", {"class": "md wiki"})

        tablemap = {}
        children = list(listings.children)

        while children[0].name != "h3":
            children.pop(0)

        current_title = ""
        current_tables = []
        while len(children) > 0:
            element = children.pop(0)
            if element.name == "h3":
                if current_title != "":
                    tablemap[current_title] = current_tables
                current_title = element.text
                current_tables = []
            elif element.name == "table":
                current_tables.append(element)

        data = []
        seasonal_mal_ids = self.get_seasonal_mal_ids(year, season)

        for title, tables in tablemap.items():

            if title not in selected_series:
                continue

            print("Loading data for {}...".format(title))
            mal_id = self.resolve_mal_id(title, seasonal_mal_ids)
            mal_data = self.load_mal_data(mal_id)

            rows = []
            for table in tables:
                rows += table.find_all("tr")

            for row in rows:
                columns = row.find_all("td")
                if len(columns) == 0:
                    continue
                description = columns[0].text

                try:
                    link = columns[1].find("a")["href"]
                except TypeError:  # Avoid missing links
                    continue

                if not description:
                    continue

                entry = {
                    "show": title,
                    "type": description.split("\"", 1)[0].strip(),
                    "song": description.split("\"", 1)[1].rsplit("\"", 1)[0],
                    "link": link
                }
                entry["filename"] = "{} {} - {}".format(
                    title, entry["type"], entry["song"]
                )
                entry["webm_file"] = os.path.join(
                    self.args.out, "webm", entry["filename"] + ".webm"
                )
                entry["mp3_file"] = os.path.join(
                    self.args.out, "mp3", entry["filename"] + ".mp3"
                )
                entry["cover_file"] = os.path.join(
                    self.args.out, "covers", entry["filename"] + ".jpg"
                )

                for key, value in mal_data.items():
                    entry[key] = value

                song_info = self.resolve_song_info(entry)
                entry["song_info"] = song_info

                data.append(entry)

        # load data from last year if season is Winter
        if include_previous_season and season == "Winter":
            previous_season_data = \
                self.load_data(year - 1, "Fall", selected_series, False)
            return previous_season_data + data
        else:
            return data

    @staticmethod
    def get_seasonal_mal_ids(year: int, season: str) -> Dict[str, int]:
        """
        Retrieves the myanimelist IDs for every show in an entire season
        :param year: The year of the season to check
        :param season: The season to check
        :return: A dictionary mapping series titles to myanimelist IDs
        """
        url = "https://api.jikan.moe/v3/season/{}/{}".format(
            year, season.lower()
        )
        resp = aggressive_request(url)
        info = json.loads(resp)["anime"]

        malmap = {}
        for entry in info:
            malmap[entry["title"]] = entry["mal_id"]

        # Special Cases:
        if year >= 2019:
            malmap["Fruits Basket"] = 38680

        return malmap

    @staticmethod
    def resolve_mal_id(series: str, seasonal_mal_ids: Dict[str, int]) \
            -> int:
        """
        Finds out the myanimelist ID of a series
        :param series: The series for which to get the myanimelist ID for
        :param seasonal_mal_ids: The previously fetched seasonal MAL IDs
        :return: The myanimelist ID
        """

        mal_id = seasonal_mal_ids.get(series)
        if mal_id is not None:
            return mal_id

        url = "https://api.jikan.moe/v3/search/anime/?q={}&page=1"\
            .format(series)
        resp = aggressive_request(url)
        mal_id = json.loads(resp)["results"][0]["mal_id"]

        return mal_id

    @staticmethod
    def load_mal_data(mal_id: int) -> Dict[str, Any]:
        """
        Loads information about a myanimelist ID
        :param mal_id: The myanimelist ID to check
        :return: The information fetched from myanimelist
        """
        url = "https://api.jikan.moe/v3/anime/{}".format(mal_id)
        resp = aggressive_request(url)
        info = json.loads(resp)

        song_info = {"opening_themes": [], "ending_themes": []}
        for song_type in song_info.keys():
            for song in info[song_type]:
                title = song.split("\"", 2)[1]
                artist = song.split("\"", 2)[2] \
                    .replace("by ", "") \
                    .split("(")[0]\
                    .strip()
                episodes = song.split("\"", 2)[2].split("(")
                if len(episodes) > 1:
                    episodes = episodes[1].split(")")[0].strip()
                else:
                    episodes = ""
                song_info[song_type].append((title, artist, episodes))

        return {
            "mal_id": mal_id,
            "mal_title": info["title"],
            "mal_cover": info["image_url"],
            "mal_openings": song_info["opening_themes"],
            "mal_endings": song_info["ending_themes"]
        }

    @staticmethod
    def resolve_song_info(song: Dict[str, Any]) -> Tuple[str, str, str]:
        """
        Resolves the song information for a song
        :param song: The song to get the info for
        :return: The song title, artist, episodes
        """

        song_type = song["type"].upper().split(" ")[0]
        if "OP" in song_type:
            theme_list = song["mal_openings"]
        elif "ED" in song_type:
            theme_list = song["mal_endings"]
        else:
            return "Unknown", "Unknown", "Unknown"

        number = song_type.replace("OP", "").replace("ED", "")
        if number == "":
            number = "1"
        number = int(number)

        if len(theme_list) >= number:
            return theme_list[number - 1]
        else:
            return "Unknown", "Unknown", "Unknown"

    @staticmethod
    def resolve_selected_songs(
            selected_series: List[str],
            data: Dict[str, List[Dict[str, str]]]
    ) -> List[Dict[str, str]]:
        """
        Retrieves a list of all songs that are included in a
        selection of series
        :param selected_series: The selection of series
        :param data: The song data from reddit
        :return: The list of selected songs
        """
        selected_songs = []
        for series in selected_series:
            selected_songs += data[series]
        return selected_songs

    @staticmethod
    def download_webms(selected_songs: List[Dict[str, Any]]):
        """
        Downloads a selection of webm songs
        :param selected_songs: The selection of songs to download
        :return: None
        """
        while len(selected_songs) > 0:

            retry = []

            for song in selected_songs:
                webmfile = song["webm_file"]
                # command = ["wget", song["link"], "-O", webmfile]
                command = ["curl", "-o", webmfile, song["link"]]

                if os.path.exists(webmfile) \
                        and os.path.getsize(webmfile) > 1000:
                    # Skip existing files
                    continue

                time.sleep(1)
                code = execute_command(command)
                if code != 0:
                    # We can circumvent 520 errors by requesting the videos in
                    # firefox.
                    # I have no clue why this is, I'm gussing this is due to
                    # caching on the host side
                    time.sleep(5)
                    execute_command(["firefox", song["link"]])
                    time.sleep(5)
                    code = execute_command(command)
                    if code != 0:
                        retry.append(song)

            selected_songs = retry

            if len(retry) > 0:
                print("Waiting 15s")
                time.sleep(15)

    @staticmethod
    def convert_to_mp3(selected_songs: List[Dict[str, Any]]):
        """
        Converts a selection of webm songs to mp3
        :param selected_songs: The selection of songs to convert
        :return: None
        """
        for entry in selected_songs:

            webm_file = entry["webm_file"]
            mp3_file = entry["mp3_file"]
            command = [
                "ffmpeg",
                "-i", webm_file,
                "-vn",
                "-ab", "160k",
                "-ar", "44100",
                "-y", mp3_file
            ]

            if not os.path.exists(mp3_file):
                execute_command(command)

    def generate_artist_album_structure(
            self,
            selected_songs: List[Dict[str, Any]]
    ):
        """
        Generates a folder structure for OPs and EDs following the scheme:
            Artist
            - Album
              - Song
        Songs are copied from the mp3 directory.
        :param selected_songs: The song data
        :return: None
        """
        structure_dir = os.path.join(self.args.out, "structured")
        if os.path.isdir(structure_dir):
            shutil.rmtree(structure_dir)
        os.makedirs(structure_dir)

        ops = list(filter(lambda x: "OP" in x["type"], selected_songs))
        eds = list(filter(lambda x: "ED" in x["type"], selected_songs))

        for oped_type, songs in [("OP", ops), ("ED", eds)]:
            oped_dir = os.path.join(structure_dir, oped_type)
            os.makedirs(oped_dir)

            artists = {}

            for song in songs:
                artist = song["song_info"][1]
                if artist in artists:
                    artists[artist].append(song)
                else:
                    artists[artist] = [song]

            for artist, artist_songs in artists.items():
                artist_dir = os.path.join(oped_dir, artist)
                makedirs(artist_dir)
                albums_metadata = []

                for song in artist_songs:
                    mp3_file = song["mp3_file"]
                    webm_file = song["webm_file"]
                    album = song["song"]
                    title = song["filename"]

                    album_dir = os.path.join(artist_dir, album)
                    song_path = os.path.join(album_dir, title + ".mp3")
                    vid_path = os.path.join(album_dir, title + "-video.webm")

                    makedirs(album_dir)
                    if not os.path.isfile(song_path):
                        shutil.copyfile(mp3_file, song_path)
                    if not os.path.isfile(vid_path):
                        shutil.copyfile(webm_file, vid_path)

                    anilist_id = AnilistApi().get_anilist_id_from_mal_id(
                        MediaType.ANIME, song["mal_id"]
                    )
                    albums_metadata.append({
                        "name": song["song"],
                        "series_ids": {
                            "myanimelist": [str(song["mal_id"])],
                            "anilist": [anilist_id]
                        },
                        "genre": "Anime",
                        "year": int(self.args.year),
                        "album_type": "theme_song",
                        "theme_type": oped_type
                    })

                metadir = os.path.join(artist_dir, ".meta")
                icondir = os.path.join(metadir, "icons")
                makedirs(metadir)
                makedirs(icondir)

                musicbrainzngs.set_useragent(
                    "toktokkie media manager",
                    version,
                    "https://gitlab.namibsun.net/namibsun/python/toktokie"
                )
                artist_guess = musicbrainzngs.search_artists(artist)
                if artist_guess["artist-count"] > 0:
                    artist_id = [artist_guess["artist-list"][0]["id"]]
                else:
                    artist_id = ["0"]

                metadata = {
                    "type": "music",
                    "tags": [],
                    "ids": {"musicbrainz": artist_id},
                    "albums": albums_metadata
                }
                MusicArtist(artist_dir, json_data=metadata).write()
