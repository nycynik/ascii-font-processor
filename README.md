# ascii-font-processor
This is a project for vieweing figlet formatted fonts.  It reads a folder full of 
fonts, and then allows them to be editor and viewed. 

# What is it?

I found http://www.jave.de/figlet/figfont.html.  Using [pyfiglet](https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/) this reads figlet style fonts and using PySimpleGUI it displays the fonts. 

## font book format (output format)

Each file is a collection of fonts, a font book, that is a json format with a block for each font, that includes all the meta data of the fonts in an easy to parse way for programs that want to translate text to ascii fonts.

# Contributing Fonts

Please contribute fonts! But please add attributions! Please only add fonts you own, or you know are in the public domain and add the attribution to the meta data in the font file.

Fonts must be format of figlet linked above.

