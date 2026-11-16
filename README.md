# H5P Import

## Import wordlist into dialog or flash cards

The [H5P dialog-cards](https://h5p.org/dialog-cards) are a good way of memorizing vocabulary
or similar content. However, when you have to create a list of dialogue cards in Moodle this
starts into a lot of clicking to add one entry at a time. An easier way is to have the word
list in a spreadsheet table and import it from there. This makes the handling a lot easier.
The script `import-cards.py` does this on the command line. Requirements are a installed
Python, an Open Office or Excel document and a H5P dialog-card or H5P flash-card file (you can
download an example from H5P.org). While dialog cards just allow text and easy flipping for
self controlled learning, flash cards allow the user to type in the answer. Also, images
are supported in flashcards (but not with this script).

Having a spreadsheet document with a list of answer/responses in two columns and the h5p
file, the creating of the dialog cards is done this way:

```
./import-cards.py dialog-cards-620.h5p Vocabulary.ods --title 'My beginners vocabulary'
```

The script takes arguments for the columns for the front and the back side of the dialog
card (default these are column A and B, columns letters can be provided with `--font X`
and `--back Y` to tell the script in which columns the data is located in). Also header
rows might be skipped with the argument `--row N` starting at line _N_ when the data is
preprended with headlines and column headers. A full list of arguments can be seen with
`--help`. The mandatory arguments are both files, first the H5P file, second the ODS file.

### GUI Wrapper

There is a GUI wrapper `import-cards-gui.py`, written in Python with TK, so that this
script should work on Linux, Windows and MacOS. The controls depend on the look an feel
of the OS. The script basically controls the above command line tool by offering
controls for each of the possible arguments.

To make things even easier for Windows user, the GUI wrapper in Python can be launched
with `import-cards-gui.bat` (via double click) which first checks the installed Python
environment, then checks whether the required libraries are installed and then launches
the GUI script to show the dialogue.
