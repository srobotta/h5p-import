# H5P Import

For some H5P elements the configuration and content creation is very tedious because many
clicks and repeating steps have to be done. The scripts in this repo try to speed up
the process. The use case is: a teacher has word lists (vocabulary) for a foreigh language or
technical terms that need to be memorized. The [H5P Dialog Cards](https://h5p.org/dialog-cards),
[H5P Flashcards](https://h5p.org/flashcards) are suited. In the
[H5P Quiz (Question Set)](https://h5p.org/question-set) the
[H5P Fill in the Banks](https://h5p.org/fill-in-the-blanks) question type can be used.

The wordlist itself can be managed in a spreadsheet document.

## Import wordlist into dialog or flash cards

The script `import-cards.py` does the import on the command line. Requirements, that need
to be installed are Python, an Open Office or Excel document and a H5P dialog-card,
H5P flash-card file or a H5P Quiz with at least one Fill in the Blanks question (you can
download an example from H5P.org). While dialog cards just allow text and easy flipping for
self controlled learning, flash cards allow the user to type in the answer. Also, images
are supported in flashcards (but not with this script).
The Quiz with the fill in the blanks works similar like the flash cards, the user may
type the answer as well.

Having a spreadsheet document with a list of answer/responses in two columns and the h5p
file, the creating of the dialog cards is done this way:

```
./import-cards.py dialog-cards-1129.h5p words.ods --title 'My beginners vocabulary'
```

The script takes arguments for the columns for the front and the back side of the dialog
card (default these are column A and B, columns letters can be provided with `--font X`
and `--back Y` to tell the script in which columns the data is located in). Also header
rows might be skipped with the argument `--row N` starting at line _N_ when the data is
preprended with headlines and column headers. A full list of arguments can be seen with
`--help`. The mandatory arguments are both files, first the H5P file, second the ODS file.

## GUI Wrapper

There is a GUI wrapper `import-cards-gui.py`, written in Python with TK, so that this
script should work on Linux, Windows and MacOS. The controls depend on the look an feel
of the OS. The script basically controls the above command line tool by offering
controls for each of the possible arguments.

To make things even easier for Windows user, the GUI wrapper in Python can be launched
with `import-cards-gui.bat` (via double click) which first checks the installed Python
environment, then checks whether the required libraries are installed and then launches
the GUI script to show the dialogue.
