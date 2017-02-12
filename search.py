#################################
# Programmer: Kenneth Sinder
# Date Created: 2017-02-10
# Filename: search.py
# Description: Main search script
#################################

import argparse
import os
import sys
from dbconnect import ConversationRetrievalService

DESCRIPTION = 'Skype conversation search tool'

class Searcher(object):

    conversation_service = None
    messages = []

    def __init__(self, conversation_service, username):
        """ (class, str) -> Searcher
        Prepares a new Searcher object by constructing the given
        `conversation_service` class (which must implement `retrieve([bool])`
        to retrieve a list of chat message dicts, and take in a username
        in its constructor) and calling `retrieve` on the service instance
        to populate messages internally.
        """
        self.conversation_service = conversation_service(username)
        self.messages = self.conversation_service.retrieve(True)

    def filter(self, string):
        """ (str) -> list of dict
        Returns a new list of chat messages only containing
        the given `string` in the message body.
        """
        return self.messages

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('username', metavar='username', type=str,
                        help='Skype username')
    args = parser.parse_args()
    searcher = Searcher(ConversationRetrievalService, args.username)
    print(searcher.filter(''))

if __name__ == '__main__':
    main()
