# TODO Test is working for simple response status code asserts, needs to figure out how to pass contains to avoid test failures.
# More functionalities need testing
from django.test import TestCase
from django.urls import reverse
from mybank.models import User
from django.contrib.auth import get_user_model


class RegistrationTestCase(TestCase):

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPassword!23',
            'password2': 'StrongPassword!23',
        })

        self.assertEqual(response.status_code, 200)


    def test_registration_with_weak_password(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password1': '12345',
            'password2': '12345',
        })
        self.assertEqual(response.status_code, 200) 
        self.assertFalse(User.objects.filter(username='testuser2').exists())
        self.assertContains(response, "This password is too short.")  