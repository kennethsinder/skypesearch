#################################
# Programmer: Kenneth Sinder
# Date Created: 2017-02-11
# Filename: dbconnect.py
# Description: SQLite3 DB Querying code for search.py
#################################

import sqlite3
import os
import sys
import datetime

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
        Returns a list of chat messages in the following format:
        [
            {'display_name': '___', 'username': '___', 'local_datetime': '2016-01-01 01:01:01',
            'message': '___', 'conversation_id': ___},
            ...
        ]
        Not guaranteed to be in any specific order.
        """
        cursor = self._connection.cursor()
        cursor.execute(QueryResultConverter.query)
        return QueryResultConverter.convert(cursor.fetchall())

    def cleanup(self):
        """ () -> None
        Closes the database connection.
        """
        if self._connection is not None:
            self._connection.close()
            self._connection = None

class QueryResultConverter(object):
    
    query = "SELECT from_dispname, author, timestamp, body_xml, convo_id " + \
            "FROM Messages ORDER BY timestamp DESC"

    @staticmethod
    def convert(L):
        """ (list of tuple) -> list of dict
        Database results converter used internally.
        """
        result = []
        for row in L:
            message = {}
            message['display_name'] = row[0]
            message['username'] = row[1]
            message['local_datetime'] = QueryResultConverter._convert_timestamp_to_iso(row[2])
            message['message'] = row[3]
            message['conversation_id'] = row[4]
            result.append(message)
        return result

    @staticmethod
    def _convert_timestamp_to_iso(timestamp):
        """ (int) -> str
        Returns an ISO 8601 representation of the given
        Unix timestamp.
        """
        dt = datetime.datetime.fromtimestamp(int(timestamp))
        return dt.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    reader = ConversationRetrievalService("kenneth.sinder")
    results = reader.retrieve()
    reader.cleanup()
    print(QueryResultConverter._convert_timestamp_to_iso(1486903045))
    print("Should execute main script .\search.py instead.")
