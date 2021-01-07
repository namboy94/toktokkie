# toktokkie

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namibsun/python/toktokkie/badges/master/build.svg)](https://gitlab.namibsun.net/namibsun/python/toktokkie/commits/master)|[![build status](https://gitlab.namibsun.net/namibsun/python/toktokkie/badges/develop/build.svg)](https://gitlab.namibsun.net/namibsun/python/toktokkie/commits/develop)|

![Logo](resources/logo/logo-readme.png)

The toktokkie media manager consists of a collection of command-line tools used
for keeping track of media on local storage

Currently, the following media types are supported:

- Book
- Book Series
- Movie
- TV Series
- Comic
- Visual Novels
- Music

## Structure

The metadata for a Media directory is stored inside the ```.meta```
subdirectory in a file called ```info.json```. Additionally, folder icons may
be stored in ```.meta/icons```. Depending on the metadata type, additional
special folder may exist.

## Generating and modifying metadata

To generate metadata for a media directory, run
```toktokkie metadata-gen <media_type> <directories...>```

Metadata can be modified using a text editor or the ```toktokkie metadata-add```
utility.

# Functionality:

toktokkie provides the following functionality:

    album-art-fetch     Loads music album art based on stored IDs
    anitheme-dl         Downloads anime theme songs
    archive             Archives the folder structure and metadata
    iconize             Applies folder icons
    id-fetch            Fills out IDs based on existing IDs
    manga-create        Creates a new manga directory based on anilist/mangadex data
    metadata-add        Adds data to existing metadata
    metadata-gen        Creates new metadata configuration for a directory
    metadata-validate   Verifies if a directory is a valid toktokkie metadata directory
    music-merge         Combines multiple music directories into one
    music-tag           Modifies the mp3 music tags based on metadata
    playlist-create     Creates a playlist file containingall songs in the directories
    print               Prints the metadata of a directory
    rename              Renames directory content based on IDs
    set-comic-cover     Creates a comic cover cbz file
    supercut            Allows creation of supercuts of tv shows
    update              Updates directory with new episodes/chapters etc
    urlopen             Opens the stored IDs in a browser
    youtube-music-dl    Downloads music from youtube

## Further Information

* [Changelog](CHANGELOG)
* [License (GPLv3)](LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namibsun/python/toktokkie)
* [Github](https://github.com/namboy94/toktokkie)
* [Progstats](https://progstats.namibsun.net/projects/toktokkie)
* [PyPi](https://pypi.org/project/toktokkie)
