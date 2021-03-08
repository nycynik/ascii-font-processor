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


def show_font_editor(settings, fonts):

    column_left = [[sg.Table(headings=['Font Name'], values=fonts, key='-font-list-',
                             col_widths=[40], num_rows=30, enable_events=True), sg.VerticalSeparator(pad=((5, 5), 0))]
                   ]
    column_right = [[sg.Text("Font Name:"), sg.Input(key='-font-name-')],
                    [sg.Multiline(size=(20, 10), key='-font-info-')],
                    [sg.Multiline(size=(25, 20), key='-OUTPUT-',
                                  font=('Courier', '12'))],
                    ]

    col1 = sg.Column(column_left)
    col2 = sg.Column(column_right)

    layout = [[col1,  col2],
              [sg.Button('Show'), sg.Button('Exit')]]

    window = sg.Window('Font Viewer', layout, auto_size_text=True,
                       auto_size_buttons=True, resizable=True, grab_anywhere=False,
                       border_depth=5, default_element_size=(15, 1), finalize=True)

    col1.expand(False, False)
    # layout[0][1].expand(False, False)
    col2.expand(True, True)
    window['-font-list-'].expand(expand_y=True,
                                 expand_x=False, expand_row=True)
    window['-OUTPUT-'].expand(True, True, expand_row=True)
    window['-font-info-'].expand(True, False)

    while True:  # Event Loop
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Save':
            pass
        if event == '-font-list-':
            # first one is the selected, no multi-select allowed.
            selected_font = fonts[values['-font-list-'][0]]
            window['-font-name-'].update(selected_font)
            window['-font-info-'].update(fontBook.get_info(selected_font))
            window['-OUTPUT-'].update(
                fontBook.draw_text(selected_font, selected_font))

    window.close()


def main_parser(settings):
    # TODO: Update it to also check for fonts in specified
    # folders. settings['font_folder']
    fonts = fontBook.list_all_fonts()
    show_font_editor(settings, fonts)


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
    parser.add_argument('-q', '--quiet', action='store_true')

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


if __name__ == "__main__":
    main()
