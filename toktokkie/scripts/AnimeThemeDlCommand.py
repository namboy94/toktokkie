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
import shutil
import argparse
from typing import Dict, List
from bs4 import BeautifulSoup
from toktokkie.scripts.Command import Command
from toktokkie.metadata.MusicArtist import MusicArtist
from puffotter.os import makedirs, listdir
from puffotter.requests import aggressive_request
from toktokkie.scripts.RenameCommand import RenameCommand
from toktokkie.scripts.PlaylistCreateCommand import PlaylistCreateCommand
from toktokkie.scripts.AlbumArtFetchCommand import AlbumArtFetchCommand
from toktokkie.scripts.MusicTagCommand import MusicTagCommand
from toktokkie.anithemes.AniTheme import AniTheme


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
        selected_songs = AniTheme.load_reddit_anithemes_wiki_info(
            self.args.year,
            self.args.season,
            selected_series
        )
        selected_songs = list(filter(
            lambda x: not x.alternate_version,
            selected_songs
        ))
        selected_songs = self.handle_excludes(selected_songs)

        for song in selected_songs:
            song.download_webm()
            song.convert_to_mp3()

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
            selected_songs: List[AniTheme]
    ) -> List[AniTheme]:
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
                print("[{}]: {}".format(i + 1, song))

            while True:

                selection = \
                    input("Please select the songs to exclude: ").strip()

                if selection == "":
                    excludes = []
                    break
                try:
                    selection = selection.strip().split(",")
                    excludes = list(map(
                        lambda x: selected_songs[int(x) - 1].filename,
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
            if song.filename not in excludes:
                new_selection.append(song)

        return new_selection

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

    def generate_artist_album_structure(
            self,
            selected_songs: List[AniTheme]
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

        ops = list(filter(lambda x: "OP" in x.theme_type, selected_songs))
        eds = list(filter(lambda x: "ED" in x.theme_type, selected_songs))

        for oped_type, songs in [("OP", ops), ("ED", eds)]:
            oped_dir = os.path.join(structure_dir, oped_type)
            os.makedirs(oped_dir)

            artists = {}

            for song in songs:
                if song.artist in artists:
                    artists[song.artist].append(song)
                else:
                    artists[song.artist] = [song]

            for artist, artist_songs in artists.items():
                artist_dir = os.path.join(oped_dir, artist)
                makedirs(artist_dir)
                albums_metadata = []

                for song in artist_songs:
                    mp3_file = song.temp_mp3_file
                    webm_file = song.temp_webm_file
                    album = song.song_name
                    title = song.filename

                    album_dir = os.path.join(artist_dir, album)
                    song_path = os.path.join(album_dir, title + ".mp3")
                    vid_path = os.path.join(album_dir, title + "-video.webm")

                    makedirs(album_dir)
                    if not os.path.isfile(song_path):
                        shutil.copyfile(mp3_file, song_path)
                    if not os.path.isfile(vid_path):
                        shutil.copyfile(webm_file, vid_path)

                    albums_metadata.append({
                        "name": song.song_name,
                        "series_ids": {
                            "myanimelist": [str(song.mal_id)],
                            "anilist": [str(song.anilist_id)]
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

                metadata = {
                    "type": "music",
                    "tags": [],
                    "ids": {"musicbrainz": ["0"]},
                    "albums": albums_metadata
                }
                MusicArtist(artist_dir, json_data=metadata).write()
