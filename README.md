# SkypeSearch

![coverage badge](https://cdn.rawgit.com/kennethsinder/skypesearch/master/coverage.svg)

Command-line script to search for a particular string in group conversations created by Skype (in local sqlite3 db).
Skype for Linux does not support group chats, so for now this only works on Windows.

Currently WIP.

## Getting Started

1. Make sure Python 3 is installed on your machine.

2. `cd` into the directory you downloaded and extracted SkypeSearch into.

3. From a Windows command prompt: `chcp 65001`

4. `set PYTHONIOENCODING=utf-8`

3. `python search.py [-h] username query`, and follow the on-screen instructions.

4. Enjoy searching for old Skype messages you thought everyone forgot about! :)