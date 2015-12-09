"""
Main script
@author Hermann Krumrey
"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cli", help="Starts the program in CLI mode", action="store_true")
parser.add_argument("-d", "--directory", help="Starts the program and renames using a single directory")
args = parser.parse_args()

if args.cli:
    print("start cli")
else:
    print("start gui")