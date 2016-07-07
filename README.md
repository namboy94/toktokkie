# Tok Tokkie Media Manager

This is a program which allows convenient managing of various Media collections, mostly Videos. The program is written
in python 3 and won't normally run on python 2. However, a version converted using 3to2 is available on the python
package index (Link below).

[Changelog](http://gitlab.namibsun.net/namboy94/tok-tokkie/raw/master/CHANGELOG)

## Main features

**Renaming Episodes**

The Renaming feature of Tok Tokkie Media Manager allows the user to specify a directory. Every subdirectory of this directory
will be checked for a .icons subdirectory. If a .icons subdirectory is present, all of the sibling subdirectories'
children files will be renamed using data from thetvdb.com in the format:

    Show Name - SXXEXX - Episode Name

An example:

    -- user-provided directory
     |-- directory 1
     |  |-- subdirectory 1
     |     |-- Season 1
     |	   |   |-- [TV]Super_Hyper_Interesting_TV_Show_01
     |	   |   |-- [TV]Super_Hyper_Interesting_TV_Show_02
     |	   |   |-- [TV]Super_Hyper_Interesting_TV_Show_03
     |	   |   |-- [TV]Super_Hyper_Interesting_TV_Show_04
     | 	   |-- .icons
     | 	   |-- Specials
     |-- directory 2
        |-- Season 1
        |   |-- Episode 1
        |   |-- Episode 2
        |   |-- Episode 3
        |   |-- Episode 4
        |-- Season 3
        |   |-- Episode 1
        |-- .icons

Given this directory tree, the directories 'subdirectory 1' and 'directory 2' will be used for renaming, as they
both contain a .icons subdirectory.

All other subdirectories' children (Episode 1, Episode 2, [TV]Super_Hyper_Interesting_TV_Show_01 etc.) will now be
renamed.

The information is determined like this:

Show Name:  This is the name of the parent directory of the .icons directory, in this case it would be 'directory 2'
or 'subdirectory 1'

Season Number:  This is determined by the individual subdirectory's names. For Example, 'Season 1' results in 1,
'Season 3' in 3. All directories that can't be parsed like this ('Specials', for example) are assigned the season
number 0.

Episode Number:  The alphabetical position of the file in the Season folder

Episode Name:  Determined by the database on thetvdb.com using the other gathered information

**Iconizing Directories**

The program can also automatically set folder icon properties of directories containing a .icons subdirectory.
The .icons directory can contain icon files (.png for normal operating systems, .ico for Windows) that match the name
of the other subdirectories. The exception to this rule is the main.png/main.ico file, which will be used to iconize the
parent directory.

An Example:

    -- user-provided directory
     |-- directory 1
       |-- subdirectory 1
          |-- Season 1
     	   |   |-- English
     	   |   |-- German
      	   |-- .icons
           |   |-- main.png
           |   |-- German.png
           |   |-- English.png
           |   |-- Season 1.png
           |   |-- Specials.png
      	   |-- Specials

This will set the folder icon of 'subdirectory 1' to '.icons/main.png', 'Season 1' to '.icons/Season 1.png',
'German' to '.icons/German.png' and so forth.

This is currently supported under Windows and Linux file managers that support gvfs metadata.

**Batch Download Manager**

The Batch Download Manager (BDLM from now on) can be used to download files via the XDCC protocol normally used in conjunction with
IRC networks. The BDLM also support searching for files on three different packlist search engines:

* xdcc.horriblesubs.info
* NIBL.co.uk
* intel.haruhichan.com
* ixIrc.com

By being provided metadata by the user, the BDLM can also rename and iconize newly downloaded files and created 
directories using the same mechanisms described above.

It is possible to select more than one file to download (hence the 'batch')

**Show Manager**

This will be able to manage your existing media in some way. It's not implemented yet.


## Standalone Scripts

The Program also offers a few standalone CLI tools:

**xdcc-dl**
This script can be used to instantly download a xdcc-get formatted pack string, like this:

    /msg BOT xdcc send #PACK
    
**anime-updater**

This is an automatic downloader for anime series. It downloads all currently available episodes for a
specified show.

To specify the setting of the shows to download, modify [this python file](tok_tokkie/templates/anime-updater-config.py) to your liking and run it.

## Installation

To install the program, either download the source and run

    # python setup.py install
    
or install using pip:

    # pip install toktokkie

Windows Builds are available [here](http://gitlab.namibsun.net/namboy94/tok-tokkie/wikis/windows-builds)

## Contributing

This project is automatically mirrored to [github](https://github.com/namboy94/toktokkie), however all development
is conducted at a privately hosted [Gitlab instance](http://gitlab.namibsun.net/namboy94/tok-tokkie). Issues
on both services are taken unto consideration.

## Documentation

Sphinx Documentation can be found [here](http://krumreyh.eu/toktokkie/documentation/html/index.html).
A [PDF version](http://krumreyh.eu/toktokkie/documentation/documentation.pdf) is also available

## Statistics

Automatically generated git statistics can be found [here](http://krumreyh.eu/toktokkie/git_stats/index.html)


## Disclaimer:

The developer(s) of this software is/are not liable for any unlawful use of the provided software.