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
from typing import Union, List
from subprocess import check_output, Popen
from toktokkie.Directory import Directory
from toktokkie.commands.Command import Command
from toktokkie.enums import MediaType
from toktokkie.metadata.tv.Tv import Tv
from toktokkie.metadata.movie.Movie import Movie
from puffotter.os import get_ext
from puffotter.init import argparse_add_verbosity


class VideoReEncodeCommand(Command):
    """
    Class that encapsulates behaviour of the video-re-encode command
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The command name
        """
        return "video-re-encode"

    @classmethod
    def help(cls) -> str:
        """
        :return: The help message for the command
        """
        return "Allows re-encoding videos files using ffmpeg"

    @classmethod
    def prepare_parser(cls, parser: argparse.ArgumentParser):
        """
        Prepares an argumentparser for this command
        :param parser: The parser to prepare
        :return: None
        """
        cls.add_directories_arg(parser)
        encoding_parser = parser.add_subparsers(
            dest="codec", help="The target encoding"
        )
        encoding_parser.required = True

        hevc_parser = encoding_parser.add_parser("hevc")
        hevc_parser.add_argument("--pixel-format", default="yuv420p10le",
                                 help="The pixel format. Defaults to 10 bit")
        hevc_parser.add_argument("--nvidia", action="store_true",
                                 help="Uses nvidia hardware encoding")
        hevc_parser.add_argument("--quality", default=18, type=int,
                                 help="The crf value (lower=better quality)")
        argparse_add_verbosity(hevc_parser)

        # parser.add_argument("--anilist-reduce")

    def execute(self):
        """
        Executes the command
        :return: None
        """
        directories = Directory.load_directories(
            self.args.directories,
            restrictions=[MediaType.TV_SERIES, MediaType.MOVIE]
        )
        for directory in directories:
            metadata = directory.metadata

            if "no_re_encode" in metadata.tags:
                self.logger.info(f"Skipping {metadata.name}")
                continue

            video_files = self.gather_videos(metadata)
            for video_file in reversed(video_files):
                # We go in reverse order to ensure that the newest files are
                # converted first.
                # This is done to reduce risk of accidents, since newer
                # files are probably easier to recover.
                # Also, newer files are probably bigger, increasing the
                # value of re-encoding
                self.re_encode(video_file)

    @staticmethod
    def gather_videos(metadata: Union[Tv, Movie]) -> List[str]:
        """
        Collects all video file paths for a metadata object
        :param metadata: The metadata for which to collect the files
        :return: The collected video file paths
        """
        video_files = []
        if isinstance(metadata, Tv):
            for season in metadata.seasons:
                video_files += season.episode_files
        elif isinstance(metadata, Movie):
            video_files.append(metadata.movie_path)
        return video_files

    @staticmethod
    def get_current_encoding(path: str) -> str:
        """
        Retrieves the current encoding of a video file
        :param path: The path to the file
        :return: The current encoidng of the file
        """
        return check_output([
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=codec_name",
            "-of", "default=noprint_wrappers=1:nokey=1",
            path
        ]).decode("utf-8").strip()

    def re_encode(self, video_file: str):
        """
        Re-encodes a video file
        :param video_file: The video file to re-encode
        :return: None
        """
        current_encoding = self.get_current_encoding(video_file)
        if current_encoding == self.args.codec:
            self.logger.info(f"Skipping {video_file}")
            return

        out_file = os.path.join(
            os.path.dirname(video_file),
            os.path.basename(video_file).rsplit(".", 1)[0] +
            "-re_encode." + get_ext(video_file)
        )
        if os.path.isfile(out_file):
            os.remove(out_file)

        encoder = self.generate_encoder(video_file, out_file)
        print(f"Re-Encoding {video_file} "
              f"from {current_encoding} to {self.args.codec}")
        self.logger.info(" ".join(encoder))
        Popen(encoder).wait()
        if os.path.isfile(out_file):
            os.remove(video_file)
            os.rename(out_file, video_file)
        else:
            self.logger.warning(f"Failed to re-encode {video_file}")

    def generate_encoder(self, input_file: str, output_file: str) -> List[str]:
        """
        Creates the encoder command for the selected codec
        :param input_file: The input file
        :param output_file: The output file
        :return: The encoder command
        """
        ffmpeg = ["ffmpeg", "-v", "quiet", "-stats", "-i", input_file]

        if self.args.codec == "hevc":
            ffmpeg += [
                "-c:v", "libx265" if not self.args.nvidia else "hevc_nvenc",
                "-crf", str(self.args.quality)
            ]

        ffmpeg += [
            "-c:a", "copy",
            "-c:s", "copy",
            "-map", "0",
            output_file
        ]
        return ffmpeg
