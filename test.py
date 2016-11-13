from app import app
import unittest
 
class FlaskTestCases(unittest.TestCase):
    
    def first_test(self):
        tester = app.test_client(self)
        response = app.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def second_test(self):
        tester = app.test_client(self)
        response = app.get('/', content_type='html/text')
        self.assertIn('cass')
 
if __name__ == '__main__':
    unittest.main()