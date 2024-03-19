from rest_framework.test import APITestCase

from authentication.models import User


class TestModel(APITestCase):

    def test_create_user(self):
        user = User.objects.create_user('Test User','test@example.com', 'testpass123')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'test@example.com')

    def test_create_super_user(self):
        user = User.objects.create_superuser('Test User','test@example.com', 'testpass123')
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, 'test@example.com')

    def test_raises_error_when_no_username(self):
        self.assertRaises(ValueError, User.objects.create_user, username= '', email= 'test@example.com', password= 'testpass123')

    def test_raises_error_when_no_email(self):
        self.assertRaises(ValueError, User.objects.create_user, username= 'Test User', email= '', password= 'testpass123')

    def test_creates_superuser_with_superuser_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(username= 'Test User', email= 'test@example.com', password= 'testpass123', is_superuser= False)

    def test_creates_superuser_with_superuser_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(username= 'Test User', email= 'test@example.com', password= 'testpass123', is_staff= False)