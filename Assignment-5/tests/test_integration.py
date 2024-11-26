import unittest
from app import app

class IntegrationTest(unittest.TestCase):

def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

def test_integration1(self):
    
def test_integration2(self):
    
def test_integration3(self):
    
if __name__ == '__main__':
    unittest.main()