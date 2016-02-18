# Media Manager

This is a program which allows convenient managing of various Media collections, mostly Videos.

To install the program, either download the source and run

    python setup.py install
    
or install using pip:

    pip install media_manager
    

This program is currently dependent on python-gobject, which is a GTK 3.0 interface for python.
Sadly, python-gobject is NOT available through pip, which means you'll have to install it manually
through your package manager. At least on Arch Linux, you'll have to run:

    sudo pacman -S python-gobject
    
The program currently only works on Linux, it might work on Mac OS X, but definitely not on Windows.