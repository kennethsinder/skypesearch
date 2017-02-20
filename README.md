# SkypeSearch

![coverage badge](https://cdn.rawgit.com/kennethsinder/skypesearch/master/coverage.svg)

Command-line script to search for a particular string in group conversations created by Skype (in local sqlite3 db).
Skype for Linux does not support group chats, so for now this only works on Windows.

## Getting Started

1. Make sure Python 3 is installed on your machine.

2. `cd` into the directory you downloaded and extracted SkypeSearch into.

3. From a Windows command prompt: `chcp 65001`

4. `set PYTHONIOENCODING=utf-8`. These two commands are necessary to prepare the Windows terminal for Unicode output.

3. `python search.py [-h] username query [-c]`, and follow the on-screen instructions. -h is for help and -c is for case-insensitive searching.

4. Enjoy searching for old Skype messages you thought everyone forgot about! :)

5. Pipe to `more` or some other formatting command to view output in multiple pages, as there may be a lot of results returned back.

## Ideas

* Skype creates XML when emoticons or special formatting are used in messages. Strip the tags and possibly even replace them with Unicode equivalents.

* Provide regex and other filtering options in `Seacher` in `search.py`.

* Add support for non-group conversations. Skype stores these in a different sqlite3 table.

* Auto-detect username rather than requiring manual entry.

* Improve documentation and transition to typehinted methods.

* Create GUI as alternative to command-line.

* Find a way to exclude call to unit tests and other untestable lines from coverage percentage.