import PySimpleGUI as sg
import json
import os.path
import argparse
import sys
import fontBook


def save_json(values, save_file):
    with open(save_file, 'w') as json_save_file:
        json_save_file.write(json.dumps(values))
    json_save_file.close()


def main_parser(settings):
    fonts = fontBook.load_fonts(settings['font_folder'])
    save_json(fonts, os.path.join(settings['output'], 'fontbook.json'))

    print(f"parsed fonts, found {len(fonts)} fonts.")
    print(f"Clean font has {len(fonts['clean'][fontBook.GLYPH_KEY])} glyphs.")
    pass


def main():
    """main.

    TODO: everything. """

    errors = {'no_fonts': 'Invalid Font Folder or path. Either the font folder has no fonts in it, or the folder path is invalid.'}

    sg.theme('Dark Blue 3')
    data = None

    # read the command line args.
    parser = argparse.ArgumentParser(
        description='Generate a Game Development Doc (GDD).')
    parser.add_argument(
        "-i", "--input", help="Input folder that contains font files")
    parser.add_argument('-o', '--output', default='output',
                        help='the folder to save the output')
    parser.add_argument('-l', '--log', default='log.txt',
                        help='the log file')
    parser.add_argument('-q', '--quiet', action='store_true' )

    args = parser.parse_args()

    # == verify args ==
    settings = {'log': args.log, 'quiet': args.quiet}

    # if the input folder is not a folder, get one
    if args.input is None or len(args.input.strip()) == 0 or not os.path.isdir(args.input):
        if settings['quiet'] == True:
            # no window opening, can't continue
            print(errors['no_fonts'])
            return

        # ask the user for the font folder.            
        event, values = sg.Window('Choose Font Folder', [[sg.Text('Font Folder')], [
                                  sg.Input(key='-path-'), sg.FolderBrowse()], [sg.OK(), sg.Cancel()]]).read(close=True)
        if event == 'OK':
            if '-path-' not in values or len(values['-path-'].strip()) == 0 or not os.path.isdir(values['-path-']):
                print(errors['no_fonts'])
                return
            else:
                settings['font_folder'] = values['-path-']
        else:
            print("No font folder selected.")
            # they did not enter it on the command line, and did not pick it.
            return
    else:
        settings['font_folder'] = args.input

    # if no output folder exists, we create it
    if not os.path.isdir(args.output):
        os.makedirs(args.output)
    settings['output'] = args.output

    main_parser(settings)
    print(settings)

if __name__ == "__main__":
    main()
