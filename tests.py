#################################
# Programmer: Kenneth Sinder
# Date Created: 2017-02-12
# Filename: tests.py
# Description: Unit tests
#################################

import unittest
import os
import sys
import dbconnect
import search
from dbconnect import ConversationRetrievalService, QueryResultConverter
from search import Searcher

# -----------------------------------------------------------------

class TestConversationRetrievalService(unittest.TestCase):
    """
    Tests invalid username with `ConversationRetrievalService`.
    Since the behaviour of this class is system-dependent, no other
    test cases can really be made.
    """

    def test_invalid_username(self):
        """ () -> None
        Invalid username should raise a `ValueError`
        when a service is constructed.
        """
        with self.assertRaises(ValueError):
            ConversationRetrievalService('BADUSERNAME')

# -----------------------------------------------------------------

class TestQueryResultConverter(unittest.TestCase):
    """ 
    Tests for conversations converter `QueryResultConverter`.
    """

    def test_convert_two_records(self):
        """ () -> None
        Two records from the DB should result in two
        converted records which have a converted
        datetime string.
        """
        db_output = [('ks', 'kenneth', 1461234567, 'Test message', 822)]
        db_output.append(('ks', 'kenneth', 1461234569, 'Test message 2', 822))

        result = QueryResultConverter.convert(db_output)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['message'], 'Test message')
        self.assertEqual(result[1]['conversation_id'], 822)
        self.assertTrue('2016-04-21' in result[0]['local_datetime'])

    def test_convert_zero_records(self):
        """ () -> None
        Zero records should be converted to an empty
        list of chat messages without throwing any exceptions.
        """
        result = QueryResultConverter.convert([])

        self.assertEqual(len(result), 0)

    def test_query_string(self):
        """ () -> None
        `QueryResultConverter` is SQLite3-specific, so it should
        contain an appropriate command in its `query`.
        """
        result = QueryResultConverter.query
        
        self.assertGreater(len(result), 0)
        self.assertTrue('from_dispname' in result.lower())
        self.assertTrue('SELECT' in result.upper())

# -----------------------------------------------------------------

class TestSearcher(unittest.TestCase):
    """
    Tests for `Searcher` class in `search.py`.
    """

    class DummyConversationService(object):
        MESSAGE = {'display_name': 'ks', 'username': 'ks', 'local_datetime': \
                    '2016-01-01 01:01:01', 'message': 'MyMsg', 'conversation_id': 890}
        def __init__(self, username):
            pass
        def retrieve(self, close_connection=False):
            return [self.MESSAGE]

    def test_filter_one_message_empty_query(self):
        """ () -> None
        One message with no search string should
        return one message
        """

        searcher = Searcher(self.DummyConversationService, 'irrelevant')

        result = searcher.filter()

        self.assertTrue('MyMsg' in result)
        self.assertTrue('2016-01-01 01:01:01' in result)
        self.assertTrue(5 <= result.count(os.linesep) <= 7)

    def test_filter_one_message_case_insensitive_search(self):
        """ () -> None
        One message with no search string should
        return one message
        """

        searcher = Searcher(self.DummyConversationService, 'irrelevant', True)

        result = searcher.filter('mymsg')

        self.assertTrue('MyMsg' in result)
        self.assertTrue('2016-01-01 01:01:01' in result)
        self.assertTrue(5 <= result.count(os.linesep) <= 7)

    def test_filter_one_message_no_results(self):
        """ () -> None
        One message with an unrelated search string
        should return no messages.
        """
        searcher = Searcher(self.DummyConversationService, 'irrelevant', True)

        result = searcher.filter(TestSearcher.DummyConversationService.MESSAGE['message'][::-1])

        self.assertEqual(result, str())

# -----------------------------------------------------------------

class TestSearch(unittest.TestCase):
    """
    Module-level sanity check for script `search.py`.
    """

    def test_description(self):
        """ () -> None
        Script must have a `DESCRIPTION` string, which must
        describe the script's purpose.
        """
        self.assertTrue(len(search.DESCRIPTION) > 0)
        self.assertTrue('search' in search.DESCRIPTION)

    def test_main_no_args(self):
        """ () -> None
        Tests `main()` with no arguments.
        """
        with self.assertRaises(SystemExit):
            sys.stdout = sys.stderr = open(os.devnull, 'w')
            search.main()

# -----------------------------------------------------------------

if __name__ == '__main__':
    # Sanity-check this module
    import doctest
    doctest.testmod()

    # Run unit tests
    unittest.main()
