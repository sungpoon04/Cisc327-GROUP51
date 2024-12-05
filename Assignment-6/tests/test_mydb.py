import unittest
import uuid
from app import app
import sqlite3
from database_op import insert_user,register_user, get_user_by_email, user_exists, delete_user, get_all_users, check_exist, DATABASE
from init_tables import create_user

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client with unique user data for isolation."""
        check_exist()
        self.test_email = f"unique_{uuid.uuid4()}@example.com"
        self.test_phone = f"123456{uuid.uuid4().int % 10000}"
        insert_user(self.test_email, self.test_phone, "password123", "Test", "User", "456 Unique St")

    def tearDown(self):
        """Delete the test user after each test to maintain database integrity."""
        delete_user(self.test_email)

    # Test check_exist function
    def test_check_exist(self):
        check_exist()
        users = get_all_users()
        self.assertIsInstance(users, list)

    # Test delete_user by adding, deleting, and confirming deletion
    def test_delete_user(self):
        temp_email = "temp_user@example.com"
        insert_user(temp_email, "0123456789", "password123", "Temp", "User", "123 Temp St")
        delete_user(temp_email)
        user = get_user_by_email(temp_email)
        self.assertIsNone(user)

    # Test get_all_users function
    def test_get_all_users(self):
        test_email = f"test_user_{uuid.uuid4()}@example.com"
        test_phone = f"123456{uuid.uuid4().int % 10000}"

        delete_user(test_email)
        insert_user(test_email, test_phone, 'password123', 'Test', 'User', '123 Test St')
        
        users = get_all_users()
        self.assertTrue(any(u[1] == test_email for u in users), "User email not found in database")

        delete_user(test_email)

    # Test user_exists for a non-existent user
    def test_user_exists_not_found(self):
        non_existent_email = f"nonexistent_{uuid.uuid4()}@example.com"
        non_existent_phone = f"123456{uuid.uuid4().int % 10000}"
        self.assertFalse(user_exists(non_existent_email, non_existent_phone), "Non-existent user should return False")

    # Test check_exist to ensure table creation logic is triggered if the table is missing
    def test_check_exist_creates_table_if_missing(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        conn.commit()
        conn.close()

        check_exist()
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        exist = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(exist, "The 'users' table was not created as expected.")
        
    # Test register_user with a unique email and phone number
    def test_register_user(self):
        unique_email = f"register_{uuid.uuid4()}@example.com"
        unique_phone = f"123456{uuid.uuid4().int % 10000}"

        # Use a mock request context with unique test data
        with app.test_request_context('/register', method='POST', data={
            'email': unique_email,
            'phone': unique_phone,
            'password': 'password123',
            'first-name': 'Test',
            'last-name': 'User',
            'home-address': '123 Test St'
        }):
            register_user()
            user = get_user_by_email(unique_email)
            self.assertIsNotNone(user)
            self.assertEqual(user[0], unique_email)

            # Cleanup: Delete the test user after verification
            delete_user(unique_email)

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
