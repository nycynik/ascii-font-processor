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


def get_ascii_text(selected_font, text, width=80):
    """returns the ascii font, but also accomodates the max width thanks to PySimpleGUI."""
    if text.strip() == '':
        text = selected_font.strip()
    return fontBook.draw_text(selected_font, text, width)

def show_font_editor(settings, fonts):

    LINE_LENGTH = 100
    MULTILINE_FONT = ('Courier', 12)
    selected_font = fonts[0]

    # col 1, the font selector
    column_left = [[sg.Table(headings=['Font Name'], values=fonts, key='-FONT-LIST-',
                             col_widths=[40], num_rows=30, enable_events=True), sg.VerticalSeparator(pad=((5, 5), 0))]
                   ]
    # col2, the view/details of the font
    # Thanks for the multiline scrolling update added by PySimpleGUI - https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_pyfiglet.py
    try:
        mline_input = sg.Multiline('', size=(40,3), key='-TEXT-TO-SHOW-', scrollbar=False, enable_events=True, focus=True)
    except:
        mline_input = sg.Multiline('', size=(40,3), key='-TEXT-TO-SHOW-', enable_events=True, focus=True)
    column_right = [[sg.Text("Font Name:", size=(10,1), justification="right"), sg.Input(selected_font, key='-FONT-NAME-')],
                    [sg.Text("Font Info:", size=(10,10), justification="right"), sg.Multiline(size=(20, 10), key='-FONT-INFO-')],
                    [sg.Text("Text:", size=(10, 3), justification="right"), mline_input, sg.T('Font size for display below'),
                        sg.Combo(list(range(4,20)), 12, enable_events=True,  k='-FONT-SIZE-')],
                    [sg.Multiline(size=(LINE_LENGTH, 20), key='-OUTPUT-', font=MULTILINE_FONT)],
                    ]

    col1 = sg.Column(column_left)
    col2 = sg.Column(column_right)

    layout = [[col1,  col2],
              [sg.Button('Exit'), sg.T('PySimpleGUI ver ' + sg.version.split(' ')[0] + ' tkinter ver ' + sg.tclversion_detailed + '  Python ver ' + sys.version, font='Default 8', pad=(0, 0))],
              ]

    window = sg.Window('Figlet Viewer', layout, auto_size_text=True,
                       auto_size_buttons=True, resizable=True, grab_anywhere=False,
                       border_depth=5, default_element_size=(15, 1), finalize=True)

    col1.expand(False, False)
    # layout[0][1].expand(False, False)
    col2.expand(True, True)
    window['-FONT-LIST-'].expand(expand_y=True,
                                 expand_x=False, expand_row=True)
    window['-FONT-INFO-'].expand(True, False)
    window['-FONT-INFO-'].update(fontBook.get_info(selected_font))
    window['-OUTPUT-'].expand(True, True, expand_row=True)
    window['-OUTPUT-'].update(get_ascii_text(selected_font, selected_font).strip())

    while True:  # Event Loop
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-FONT-LIST-':
            # first one is the selected, no multi-select allowed.
            selected_font = fonts[values['-FONT-LIST-'][0]]
            window['-FONT-NAME-'].update(selected_font)
            window['-FONT-INFO-'].update(fontBook.get_info(selected_font))

        elif event == '-FONT-SIZE-':
            MULTILINE_FONT = (MULTILINE_FONT[0], values['-FONT-SIZE-'])
            window['-OUTPUT-'].update(font=MULTILINE_FONT)
            window.refresh()

        if event in ('-TEXT-TO-SHOW-', '-FONT-SIZE-', '-FONT-LIST-'):
            text = values['-TEXT-TO-SHOW-']
            if text.strip() == '':
                text = selected_font.strip()

            # fancy way of detecting the size of the multiline so the window can be resized
            # line_length = window["-OUTPUT-"].get_size()[0] // sg.Text.char_width_in_pixels(MULTILINE_FONT)
            LINE_LENGTH = window["-OUTPUT-"].get_size()[0] // sg.tkinter.font.Font(font=MULTILINE_FONT).measure('A')
            window['-OUTPUT-'].update(get_ascii_text(selected_font, text, LINE_LENGTH).rstrip())

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

    sg.theme('Dark Blue 3') # Dark Blue 3
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
