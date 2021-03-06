import PySimpleGUI as sg
import json
import os.path
import argparse


def main():
    """main.

    TODO: everything. """

    data = None
    save_file = 'gameDoc.json'

    # read the command line args.
    parser = argparse.ArgumentParser(
        description='Generate a Game Development Doc (GDD).')
    parser.add_argument('-i', '--input', default='gameDocDefault.json',
                        help='the input folder')
    parser.add_argument('-l', '--log', default='log.txt',
                        help='the log file')
    parser.add_argument('-o', '--output', default='output',
                        help='the folder to save the output')

    args = parser.parse_args()

    # == verify args ==
    template = '# {{name}} Design Doc\n'

    # if not os.path.isfolder(args.output):
    #     print(
    #         'Output folder is missing or not a folder.')

    if not os.path.isdir(args.output):
        os.makedirs(args.output)


if __name__ == "__main__":
    main()
