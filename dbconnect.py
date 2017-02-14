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
import html

class ConversationRetrievalService(object):
    """
    Service to retrieve Skype conversations.
    Implements `retrieve([bool]) -> list of dict`.
    """

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

    def __str__(self) -> str:
        """ () -> str
        Returns a string representation of this `ConversationRetrievalService`.
        """
        return "Connected to main DB at {0}".format(self._path) if self._connection is not None else "Disconnected"

    def retrieve(self, close_connection=False):
        """ ([bool]) -> list of dict
        Returns a list of chat messages in the following format:
        [
            {'display_name': '___', 'username': '___', 'local_datetime': '2016-01-01 01:01:01',
            'message': '___', 'conversation_id': ___},
            ...
        ]
        Not guaranteed to be in any specific order.
        Also closes the database connection afterwards if the given flag is True
        """
        cursor = self._connection.cursor()
        cursor.execute(QueryResultConverter.query)
        result = QueryResultConverter.convert(cursor.fetchall())
        if close_connection:
            self.cleanup()
        return result

    def cleanup(self):
        """ () -> None
        Closes the database connection.
        """
        if self._connection is not None:
            self._connection.close()
            self._connection = None

class QueryResultConverter(object):
    """
    Converter from sqlite3 db output to a list
    of dictionaries. Provides the required SQL
    query.
    """

    query = "SELECT from_dispname, author, timestamp, body_xml, convo_id " + \
            "FROM Messages ORDER BY timestamp"

    @staticmethod
    def convert(tuples):
        """ (list of tuple) -> list of dict
        Database results converter used internally.
        """
        result = []
        for row in tuples:
            message = {}
            message['display_name'] = row[0]
            message['username'] = row[1]
            message['local_datetime'] = QueryResultConverter._convert_timestamp_to_iso(row[2])
            message['message'] = '' if not row[3] else html.unescape(row[3])
            message['conversation_id'] = row[4]
            result.append(message)
        return result

    @staticmethod
    def _convert_timestamp_to_iso(timestamp):
        """ (int) -> str
        Returns an ISO 8601 representation of the given
        Unix timestamp. Time will be local, not UTC, based on
        how Skype prepares the Unix timestamps.
        """
        dt = datetime.datetime.fromtimestamp(int(timestamp))
        return dt.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    print(r"Should execute main script .\search.py instead.")
