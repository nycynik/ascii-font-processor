# ascii-font-processor
This is a ascii font editor, converts ascii 'fonts' to JSON files

This project is abandoned really, as I found http://www.jave.de/figlet/figfont.html.  I might adapt this to use figlet, but I will probably never do so. Also there is [pyfiglet](https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/).

# What is it?

This is a tool that will open a folder of formatted text files that represent ascii fonts, and allow you to make a font book.  A font book in this case is a in JSON formatted file that includes the font metadata and the fonts.  This can be used for other projects that need to have ascii fonts.

## font file format (input format)

Each file is may or may not include information like height, name, fixed-width/monospaced or proportional font, and more included in the font along with the letters of the font. The format that I'm inventing may not be the best, but it is simple and easy to parse for humans. 

Goals of format:
* easy to edit in ascii editors
* easy to edit in text editors
* easy to understand for humans

## font book format (output format)

Each file is a collection of fonts, a font book, that is a json format with a block for each font, that includes all the meta data of the fonts in an easy to parse way for programs that want to translate text to ascii fonts.


# Contributing Fonts

Please contribute fonts! But please add attributions! Please only add fonts you own, or you know are in the public domain and add the attribution to the meta data in the font file.

Fonts must be format in the "font file" format explained above.
