import unittest
import dbconnect
from dbconnect import ConversationRetrievalService, QueryResultConverter

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

if __name__ == '__main__':
    unittest.main()