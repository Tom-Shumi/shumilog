from django.contrib.auth import get_user_model
from django.test import TestCase


class LoggedInTestCase(TestCase):

    def setUp(self):
        self.password = 'test00000000'
        self.test_user = get_user_model().objects.create_user(
            username='test',
            email='',
            password=self.password)

        self.client.login(username=self.test_user.username,
                          password=self.password)
