# ascii-font-processor

This is a project for vieweing figlet formatted fonts.  It reads a folder full of 
fonts, and then allows them to be editor and viewed. 

![screenshot](screenshot.png)

# What is it?

I found http://www.jave.de/figlet/figfont.html.  Using [pyfiglet](https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/) this reads figlet style fonts and using PySimpleGUI it displays the fonts. 

## Fonts

Fonts are found how figlet finds them, you may already have fonts installed on your machine, or it will search in the fonts folder int he folder it is launched in.


## Future Work

* This project was pivoted from another, so the input directory is not used currently.
* The metadata is not individually selectable from the pyFiglet library. A PR there, and then changes here would show the meta data.
* There is no way to modify the fonts, or create a font, that is a future huge project.




