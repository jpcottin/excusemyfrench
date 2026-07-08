import unittest
import json
import base64
from app import app, insultes

class ExcuseMyFrenchTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test the main page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    def test_api_v0(self):
        """Test the legacy /api route."""
        response = self.app.get('/api')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('result', data)

    def test_api_v1(self):
        """Test the /api/v1 route for correct structure."""
        response = self.app.get('/api/v1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('insult', data)
        self.assertIn('text', data['insult'])
        self.assertIn('index', data['insult'])
        self.assertIn('level', data['insult'])
        self.assertIsInstance(data['insult']['index'], int)
        self.assertIn(data['insult']['level'], (1, 2, 3))

    def test_api_v1_index_matches_dataset(self):
        """The returned index must point at the returned text in the full list."""
        response = self.app.get('/api/v1')
        data = json.loads(response.data)
        self.assertEqual(insultes[data['insult']['index']]['text'],
                         data['insult']['text'])

    def test_level_filtering(self):
        """?level=N must only serve insults of level N or below."""
        for max_level in (1, 2):
            for _ in range(30):
                response = self.app.get(f'/api/v1?level={max_level}')
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertLessEqual(data['insult']['level'], max_level)

    def test_level_default_serves_everything(self):
        """Without ?level, all three levels must be reachable."""
        seen = set()
        for _ in range(300):
            data = json.loads(self.app.get('/api/v1').data)
            seen.add(data['insult']['level'])
            if seen == {1, 2, 3}:
                break
        self.assertEqual(seen, {1, 2, 3})

    def test_invalid_level_returns_400(self):
        """Out-of-range or non-numeric levels must return 400."""
        for bad in ('0', '4', 'abc', '-1', '1.5'):
            response = self.app.get(f'/api/v1?level={bad}')
            self.assertEqual(response.status_code, 400, f'level={bad}')
        response = self.app.get('/api/v1/img?level=42')
        self.assertEqual(response.status_code, 400)

    def test_html_routes_accept_level(self):
        """HTML routes must accept the level parameter too."""
        for route in ('/', '/img', '/series'):
            response = self.app.get(f'{route}?level=1')
            self.assertEqual(response.status_code, 200, route)

    def test_api_v1_img(self):
        """Test the /api/v1/img route for base64 image data."""
        response = self.app.get('/api/v1/img')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Check insult part
        self.assertIn('insult', data)

        # Check image part
        self.assertIn('image', data)
        self.assertIn('data', data['image'])
        self.assertIn('mimetype', data['image'])
        self.assertIn('indexImg', data['image'])

        # Verify it's valid base64
        try:
            base64.b64decode(data['image']['data'])
        except Exception:
            self.fail("Image data is not valid base64")

    def test_img_route(self):
        """Test the /img HTML route."""
        response = self.app.get('/img')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'static/image/', response.data)

    def test_specific_insult_route(self):
        """Test the parameterized /img/<quo>/<img> route."""
        response = self.app.get('/img/0/0/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_specific_insult_route(self):
        """Test 404 for out of bounds indices."""
        response = self.app.get('/img/9999/9999/')
        self.assertEqual(response.status_code, 404)

    def test_favicon(self):
        """Test favicon delivery."""
        with self.app.get('/favicon.ico') as response:
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
