#
# Font editor
#
import PySimpleGUI as sg
import os
import json


def showEditor(font):
    sg.theme('DarkAmber')    # Keep things interesting for your users

    buttons = []
    button_row = []
    row_count = 0
    row_max = 10

    for c in range(65, 91):
        row_count += 1
        button_row.append(sg.Button(chr(c), size=(1, 1), key=chr(c)))
        if row_count > row_max:
            buttons.append(button_row)
            button_row = []
            row_count = 0

    if len(button_row) > 0:
        buttons.append(button_row)
    buttons.append(
        [sg.Text('Enter Character to Edit:'), sg.InputText('A', size=(2, 1))])

    a_character = "A"
    if 'A' in font:
        a_character = font['A']

    layout = [[sg.Text('Click a characer button to view or edit')],
              [sg.Frame('Characters', buttons)],
              [sg.Multiline(a_character, size=(20, 10), font=(
                  'Courier', 12), key='-CHAR-')],
              [sg.Button('Save', key='-SAVE-'), sg.Exit()]]

    window = sg.Window('Ascii Font Editor', layout, finalize=True)

    return window


def save_value(font, key, value):
    font[key] = value


def save_font(font, destination):
    with open(destination, 'w') as json_file:
        json.dump(font, json_file)


def main():

    font = {}
    cur_letter = 'A'
    destination = './output/font.json'

    if not os.path.isdir('./output'):
        os.makedirs('./output')

    window = showEditor(font)
    while True:                             # The Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif len(event) == 1:  # we assume its a char, so try it.
            save_value(font, cur_letter, values['-CHAR-'])
            print(font)
            if event in font:
                window['-CHAR-'].update(font[event])
            else:
                window['-CHAR-'].update(event)
            cur_letter = event
        elif event == '-SAVE-':
            save_font(font, destination)
            print('saved')

    window.close()


if __name__ == "__main__":
    main()
