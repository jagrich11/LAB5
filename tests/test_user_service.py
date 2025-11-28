import unittest
from unittest.mock import Mock
from models.user import User
from services.user_service import UserService
from repositories.base import UserRepository

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock(spec=UserRepository)
        self.service = UserService(self.mock_repo)

    def test_register_new_user(self):
        self.mock_repo.get_user_by_email.return_value = None
        fake_user = User(1, "Анна", "anna@example.com", None)
        self.mock_repo.create_user.return_value = fake_user

        user = self.service.register_user("Анна", "anna@example.com")
        self.assertEqual(user.name, "Анна")
        self.mock_repo.create_user.assert_called_once()

    def test_email_already_exists(self):
        existing_user = User(1, "Борис", "boris@example.com", None)
        self.mock_repo.get_user_by_email.return_value = existing_user

        with self.assertRaises(ValueError):
            self.service.register_user("Борис", "boris@example.com")

if __name__ == '__main__':
    unittest.main()
