#################################
# Programmer: Kenneth Sinder
# Date Created: 2017-02-11
# Filename: dbconnect.py
# Description: SQLite3 DB Querying code for search.py
#################################

import sqlite3
import os
import sys

class ConversationRetrievalService(object):

    _connection = None
    _path = None

    def __init__(self, username):
        """ (str) -> ConversationRetrievalService
        Requires a valid Skype `username` that has logged in
        and had conversations on this computer.
        """
        # Determine the path to the main.db file
        self._path = os.path.join(os.getenv('APPDATA'), 'skype', username, 'main.db')
        if not os.path.isfile(self._path):
            raise ValueError("{0} is not a valid username, or no main.db file exists".format(username))

        self._connection = sqlite3.connect(self._path)

    def __str__(self):
        """ () -> str
        Returns a string representation of this `ConversationRetrievalService`.
        """
        return "Connected to main DB at {0}".format(self._path) if self._connection is not None else "Disconnected"

    def retrieve(self):
        """ () -> list of dict
        Returns a list of chat messages.
        """
        cursor = self._connection.cursor()
        cursor.execute(QueryResultConverter.query)
        print(cursor.fetchone())
        return []

    def cleanup(self):
        """ () -> None
        Closes the database connection.
        """
        if self._connection is not None:
            self._connection.close()
            self._connection = None

class QueryResultConverter(object):
    
    query = "SELECT from_dispname, author, timestamp, body_xml, convo_id " + \
            "FROM Messages ORDER BY timestamp"

    def convert(L):
        """ (list of tuple) -> list of dict
        Database results converter used internally.
        """
        result = []
        for row in L:
            message = {}
            message['display_name'] = row[0]
            message['username'] = row[1]
            message['timestamp'] = row[2]
            message['message'] = row[3]
            message['conversation_id'] = row[4]
            result.append(message)
        return result

if __name__ == '__main__':
    #reader = ConversationRetrievalService("kenneth.sinder")
    #results = reader.retrieve()
    #reader.cleanup()
    print("Should execute main script .\search.py instead.")
