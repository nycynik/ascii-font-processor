import PySimpleGUI as sg
import json
import os.path
import argparse
import sys
import fontBook


def main_parser(args):
    fonts = fontBook.load_fonts(args.input)
    print(f"parsed fonts, found {len(fonts)} fonts.")
    print(f"Clean font has {len(fonts['clean'][fontBook.GLYPH_KEY])} glyphs.")
    pass


def main():
    """main.

    TODO: everything. """

    data = None
    save_file = 'gameDoc.json'

    # read the command line args.
    parser = argparse.ArgumentParser(
        description='Generate a Game Development Doc (GDD).')
    parser.add_argument("input", help="Input folder that contains font files")
    parser.add_argument('-o', '--output', default='output',
                        help='the folder to save the output')
    parser.add_argument('-l', '--log', default='log.txt',
                        help='the log file')

    args = parser.parse_args()

    # == verify args ==
    # if the input folder is not a folder, end
    if not os.path.isdir(args.input):
        print("Input folder should be a valid folder.")
    else:
        # if no output folder exists, we create it
        if not os.path.isdir(args.output):
            os.makedirs(args.output)

        # if not os.path.isfolder(args.output):
        #     print(
        #         'Output folder is missing or not a folder.')

        main_parser(args)


if __name__ == "__main__":
    main()
