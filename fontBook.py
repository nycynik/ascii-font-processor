"""fontBook utilities for ascii font parsing."""
import os
import traceback
import pyfiglet

GLYPH_KEY = 'glyphs'


def list_all_fonts():
    """Lists all system and local fonts"""

    all_fonts = pyfiglet.FigletFont.getFonts()
    return all_fonts

def get_info(font):
    """ currently wraps the infoFont call, but I would like to add a JSON represenation of this data to 
    better display the individual details of the font."""
    return pyfiglet.FigletFont.infoFont(font)
    
def draw_text(font, text):
    """Simple wrapper for the main draw function"""

    f = pyfiglet.Figlet(font=font)
    print(f.font, f.Font.comment)
    return f.renderText(text)


def parse_font_file(font_file_path):
    """Given a path to a font file, returns the parsed ascii font data

    TODO: Improve the error handling, just prints now.

    :param font_file_path: input file location, full path to file
    :return: the parsed font object or None if a problem is found
    """

    font = {GLYPH_KEY: {}}
    current_letter = ''
    in_letter = False

    try:
        all_fonts = pyfiglet.FigletFont.getFonts()
        print(all_fonts)
        return
        with open(font_file_path, 'r') as f:
            in_header = True
            for line in f:
                data = line.strip()

                # if we find a blank line, we transition to letters
                if len(data) == 0:
                    if in_header:
                        in_header = False
                    elif in_letter:
                        in_letter = False
                    continue

                if in_header:
                    k, v = data.split(':', 1)
                    if len(k) > 0 and len(v) > 0:
                        font[k.strip()] = v.strip()

                else:
                    # parsing letters.
                    if not in_letter:
                        in_letter = True
                        current_letter = data[0]
                        font[GLYPH_KEY][current_letter] = []
                        continue
                    else:
                        if current_letter in font[GLYPH_KEY]:
                            font[GLYPH_KEY][current_letter].append(data)

    except IOError as e:
        print(e)
        return None
    except Exception as e:
        print(f"A problem occured [{e}]")
        traceback.print_exc()
        return None

    return font


def load_fonts(font_dir):
    """Given a folder of figlet font files, returns data about all the font files

    :param font_dir: input folder where the fonts are located
    :return: object containing all the font data that were parsable from the folder
    """

    fonts = {}
    if os.path.isdir(font_dir):
        for filename in os.listdir(font_dir):
            # sg.one_line_progress_meter('Reading Fonts', i+1, 10000, 'key','Optional message')
            if filename.endswith(".flf"):

                font = parse_font_file(os.path.join(font_dir, filename))
                if font is not None:
                    if 'name' not in font:
                        font['name'] = filename
                    fonts[font['name']] = font

    return fonts


if __name__ == "__main__":
    print("library only.")
