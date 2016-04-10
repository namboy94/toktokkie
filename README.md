# Media Manager

This is a program which allows convenient managing of various Media collections, mostly Videos.

To install the program, either download the source and run

    python setup.py install
    
or install using pip:

    pip install media_manager
    

You can also run the main.py file directly with the python interpreter if that is how you want to do it. This will only
work when all dependencies are installed beforehand.

Check out this project's [python package index site](https://pypi.python.org/pypi/media-manager)!

The program depends on the following python packages:

- tvdb_api
- beautifulsoup4


# Installation Instructions

# GNU/Linux

install the following packages with your package manager, if you have not done so already:

- python
- tk (for Tk)
- python-gobject (for GTK)
- hexchat (optional)

These package names are the package names for pacman, Arch Linux's package manager. On other distributions,
the package names may differ.

Preferably configure a fresh hexchat config like this:

1. Skip Network List on Startup
2. Settings/Preferences/Network/File transfers/Auto Accept File Offers: Save without interaction
3. Uncheck "Always show this dialog after connecting" on first connection to a server

This is all you have to do to be able to run this program

# Windows 7+

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

And now you should be set!


Disclaimer:

The developer(s) of this software is/are not liable for any unlawful use of the provided software.

[Git Statistics](http://krumreyh.com/git_stats_pages/media-manager/general.html)

[Documentation](http://gitlab.namibsun.net/namboy94/media-manager/wikis/html/index.html)