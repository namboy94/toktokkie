import argparse

"""
Class that handles parsing of arguments
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class ArgumentParser(object):

    """
    Constructor
    Defines which options to be parsed
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-i", "--install", help="installs the program", action="store_true")
        self.parser.add_argument("-u", "--update", help="updates the program", action="store_true")
        self.parser.add_argument("-g", "--gui", help="starts the program in gui-mode", action="store_true")

    """
    Starts the argumentparser
    """
    def parse(self):
        return self.parser.parse_args()