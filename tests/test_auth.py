import unittest
from services.auth_service import login_user

class TestAuth(unittest.TestCase):

    def test_valid_login(self):
        user = login_user("admin", "admin123")
        self.assertIsNotNone(user)

    def test_invalid_login(self):
        user = login_user("wrong", "wrong")
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()