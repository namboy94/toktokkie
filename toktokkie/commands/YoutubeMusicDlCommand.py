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
import shutil
import argparse
from typing import List
from youtube_dl.YoutubeDL import YoutubeDL
from puffotter.prompt import prompt
from puffotter.os import makedirs, listdir, get_ext
from toktokkie.commands.Command import Command
from toktokkie.Directory import Directory
from toktokkie.enums import MediaType
from toktokkie.metadata.music.Music import Music
from toktokkie.metadata.music.components.MusicAlbum import MusicAlbum


class YoutubeMusicDlCommand(Command):
    """
    Class that encapsulates behaviour of the youtube-music-dl command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "youtube-music-dl"

    @classmethod
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Downloads music from youtube"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        parser.add_argument("artist_directory",
                            help="The directory of the artist")
        parser.add_argument("year", type=int, help="The year of the music")
        parser.add_argument("genre", help="The genre of the music")
        parser.add_argument("youtube_urls", nargs="+",
                            help="The youtube video/playlist URLs")
        parser.add_argument("--album-name", help="Specifies an album name for"
                                                 "the downloaded playlist")
        parser.add_argument("--only-audio", action="store_true",
                            help="If specified, discards video files")

    def execute(self):
        """
        Executes the commands
        :return: None
        """
        directories = Directory.load_directories(
            [self.args.artist_directory], [MediaType.MUSIC_ARTIST]
        )
        if len(directories) != 1:
            self.logger.warning("No valid directory provided")
            return

        directory = directories[0]
        metadata: Music = directory.metadata
        album_metadata_base = {
            "ids": {},
            "year": self.args.year,
            "genre": self.args.genre
        }

        tmp_dir = "/tmp/ytmusicdl"
        makedirs(tmp_dir, delete_before=True)

        self.download_from_youtube(tmp_dir)

        songs = {}
        for downloaded, path in listdir(tmp_dir):
            name = downloaded.replace(".mp3", "").replace("-video.mp4", "")
            if name not in songs:
                songs[name] = {}

            ext = get_ext(downloaded)
            songs["name"][ext] = path

            name = prompt(f"Enter song name for {downloaded}")
            os.rename(path, os.path.join(tmp_dir, name + ".mp3"))

        albums = []
        if self.args.album_name is not None:
            album_dir = os.path.join(directory.path, self.args.album_name)
            album_metadata_json = {"name": self.args.album_name}
            album_metadata_json.update(album_metadata_base)
            order = self.prompt_song_order(tmp_dir)
            albums.append((album_dir, album_metadata_json, order))
        else:
            for song_file, song_path in listdir(tmp_dir):
                song_name = song_file.rsplit(".mp3", 1)[0]
                album_dir = os.path.join(directory.path, song_name)
                album_metadata_json = {"name": song_name}
                album_metadata_json.update(album_metadata_base)
                albums.append((album_dir, album_metadata_json, [song_path]))

        for album_dir, album_metadata_json, songs in albums:
            if os.path.isdir(album_dir):
                self.logger.warning(f"Album {album_dir} already exists")
                continue

            makedirs(album_dir)
            for i, song in enumerate(songs):
                new_song_path = os.path.join(
                    album_dir,
                    f"{str(i + 1).zfill(2)} - {os.path.basename(song)}"
                )
                shutil.move(song, new_song_path)

            album_metadata = MusicAlbum.from_json(
                metadata.directory_path, metadata.ids, album_metadata_json
            )
            metadata.add_album(album_metadata)

        metadata.write()

    @staticmethod
    def prompt_song_order(tmp_dir: str) -> List[str]:
        """
        Prompts the user for the song order in an album
        :param tmp_dir: The directory in which the unordered files exist
        :return: List of ordered file paths
        """
        songs = os.listdir(tmp_dir)
        ordered = []

        while len(songs) > 1:
            for i, song in enumerate(songs):
                print(f"{i + 1} - {song}")
            index = prompt(
                "Next song in order: ",
                _type=int,
                choices={str(x) for x in range(1, len(songs) + 1)}
            ) - 1
            selected = songs.pop(index)
            ordered.append(selected)

        if len(songs) == 1:
            ordered.append(songs.pop(0))

        return [
            os.path.join(tmp_dir, song) for song in ordered
        ]

    def download_from_youtube(self, target_dir: str):
        makedirs(target_dir, delete_before=True)

        mp3_args = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "outtmpl": f"{target_dir}/%(title)s.%(ext)s",
            "ignoreerrors": True
        }
        mp4_args = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "outtmpl": f"{target_dir}/%(title)s-video.%(ext)s",
            "ignoreerrors": True
        }

        youtube_dl_args = [mp3_args]
        if not self.args.only_audio:
            youtube_dl_args.append(mp4_args)

        for args in youtube_dl_args:
            with YoutubeDL(args) as youtube_dl:
                youtube_dl.download(self.args.youtube_urls)
