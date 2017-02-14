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
    """
    Skype message searcher.
    Implements `filter([str]) -> str`.
    """

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

    def filter(self, string=''):
        """ ([str]) -> list of dict
        Returns a new list of chat messages only containing
        the given `string` in the message body. Default behaviour
        without `string` parameter is to return all messages unfiltered.
        """
        return os.linesep.join([self._convert_message(m) \
                for m in self.messages if string in m['message']])

    def _convert_message(self, message):
        """ (dict) -> str
        Convert a `message` represented as a dictionary to an appropriate
        string format for printing.
        """
        result = "From: {0} ({1})" + os.linesep + "Date: {2}" + \
                os.linesep + "Message: \"{3}\"" + os.linesep
        result += "Conversation ID: {4}" + os.linesep
        result = result.format(message['display_name'], message['username'], \
                message['local_datetime'], \
                message['message'], \
                message['conversation_id'])
        return result

def main():
    """ () -> None
    Main program entry point.
    """
    # Deal with the two command-line arguments
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('username', metavar='username', type=str,
                        help='Skype username')
    parser.add_argument('query', metavar='query', type=str, help='Search query')
    args = parser.parse_args()

    # Create Searcher object
    searcher = Searcher(ConversationRetrievalService, args.username)

    # Filter and print the result
    print(searcher.filter(args.query))

if __name__ == '__main__':
    main()
