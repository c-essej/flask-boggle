from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            # test that you're getting a template
            self.assertEqual(response.status_code, 200)
            self.assertIn('<title>Boggle</title>', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')

            py_dict = response.get_json()
            print(py_dict)
            # id = py_dict['gameId']
            # board = py_dict['board']
            # games = py_dict['games']
            # games ={....., {id:borad}}
            # write a test for this route
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(py_dict['gameId'], str)
            self.assertIsInstance(py_dict['board'], list)
            self.assertIsInstance(py_dict['board'][0], list)

            # self.assertIn('board', py_dict)
            # print('**** pyObj=', pyObj)
            # print('**** html=', html)

    def test_valid_word(self):
        """Test if word exists/valid on board"""

        with self.client as client:
            response = client.post('/api/score-word',
                                   data={'color': 'blue'})


