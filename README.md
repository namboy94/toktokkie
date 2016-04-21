# Media Manager

(Name subject to change until I come up with a better one)

This is a program which allows convenient managing of various Media collections, mostly Videos. The program is written
in python 3 and won't normally run on python 2. However, a version converted using 3to2 is available on the python
package index (Link below).

[Changelog](http://gitlab.namibsun.net/namboy94/media-manager/raw/master/CHANGELOG)

## Main features

**Renaming Episodes**

The Renaming feature of media manager allows the user to specify a directory. Every subdirectory of this directory
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

* NIBL.co.uk
* intel.haruhichan.com
* ixIrc.com

By being provided metadata by the user, the BDLM can also rename and iconize newly downloaded files and created 
directories using the same mechanisms described above.

It is possible to select more than one file to download (hence the 'batch')

**Show Manager**

This will be able to manage your existing media in some way. It's not implemented yet.




## Installation Instructions

**General Installation**

To install the program, either download the source and run

    python setup.py install
    
or install using pip:

    pip install media_manager
    

You can also run the main.py file directly with the python interpreter if that is how you want to do it. This will only
work when all dependencies are installed beforehand.

The program depends on the following python packages:

- tvdb_api
- beautifulsoup4
- gfworks
- typing (for python versions lower than 3.5)
- twisted (for python2)

Also needed for GUI functionality is the GUI framework Tkinter or also Python-Gobject

**Configuring Downloaders**

The Batch Download Manager currently has two different ways of downloading files via XDCC. One method, called
the Hexchat Downloader, uses Hexchat's scripting interface to download the files, while the Twisted Downloader uses
a python2 script to do this independently. Sadly, both of these methods are somewhat prone to system-specific
errors, which is why we have a rough guide on how to get them working:


*Twisted Downloader*

For the twisted downloader to work, python 2 has to be installed alongside python 3 and needs to be callable with the
command 'python2'. Additionally, the twisted package has to be installed for the python2 installation.

*Hexchat Downloader*

For the Hexchat Downloader to work, both Hexchat and the Hexchat python plugin need to be installed on the system.

## Windows Installation

Installing the program and making it work requires some more steps on Windows operating systems.

You will have to have a working python 3 installation on your machine. If you do not have this, download the file from
the [official website](https://www.python.org/downloads/windows/).

Once you have installed this, you should be able to install the program using pip or the setup.py file directly.

To update the program, either use pip or make use of
[this .bat file](http://gitlab.namibsun.net/namboy94/media-manager/raw/master/bin/update.bat).

To be able to use the Hexchat Downloader, you will have to install the 64-bit version of Hexchat for Windows from
the [official website](https://hexchat.github.io/downloads.html).

While running the installer, make sure to install the python plugin (version 3.4)!

After the installation is completed, run hexchat and set it up to your liking. The recommended procedure is this:

1. Skip Network List on Startup
2. Settings/Preferences/Network/File transfers/Auto Accept File Offers: Save without interaction
3. Uncheck "Always show this dialog after connecting" on first connection to a server

To be able to use the Twisted downloader, install python 2 and the twisted package for python 2. Also set the path
variable 'python2' to direct to the python 2 installation.

## Links:


[Git Statistics](http://gitlab.namibsun.net/namboy94/media-manager/wikis/git_stats/general.html)

[Documentation](http://gitlab.namibsun.net/namboy94/media-manager/wikis/html/index.html)

Note: Those Links need a manual refresh to load the CSS, I have no idea why.

Check out this project's python package index site:

[python 2](https://pypi.python.org/pypi/media-manager-py2)!

[python 3](https://pypi.python.org/pypi/media-manager)!



## Disclaimer:

The developer(s) of this software is/are not liable for any unlawful use of the provided software.