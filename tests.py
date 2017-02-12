import unittest
import dbconnect
import search
from dbconnect import ConversationRetrievalService, QueryResultConverter
from search import Searcher

class TestConversationRetrievalService(unittest.TestCase):
    """
    Test suite for the testable parts of `ConversationRetrievalService`.
    """

    def test_invalid_username(self):
        with self.assertRaises(ValueError):
            s = ConversationRetrievalService('BADUSERNAME')

class TestQueryResultConverter(unittest.TestCase):
    """ 
    Test suite for conversations converter.
    """

    def test_convert(self):
        db_output = [('ks', 'kenneth', 1461234567, 'Test message', 822)]
        db_output.append(('ks', 'kenneth', 1461234569, 'Test message 2', 822))

        result = QueryResultConverter.convert(db_output)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['message'], 'Test message')
        self.assertEqual(result[1]['conversation_id'], 822)
        self.assertTrue('2016-04-21' in result[0]['local_datetime'])

class TestSearch(unittest.TestCase):
    """
    Test suite for search.py.
    """

    def test_description(self):
        self.assertTrue(len(search.DESCRIPTION) > 0)
        self.assertTrue('search' in search.DESCRIPTION)

if __name__ == '__main__':
    # Run tests
    unittest.main()