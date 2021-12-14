from datetime import datetime

from django.forms import Field
from django.test import TestCase
from django.contrib.auth.models import User
from ..forms import RegisterForm, AuthForm, CreateBlogForm, FileBlogForm


class BaseFormTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.u1 = User.objects.create_user(username='test3', password='11test11', email='testuser@test.com')
        cls.valid_data = {
            'username': 'test3',
            'password1': '11test11',
            'password2': '11test11',
        }


class RegistrationFormTest(BaseFormTestCase):

    def test_user_already_exist(self):
        form = RegisterForm(self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['username'].errors,
                         [str(User._meta.get_field('username').error_messages['unique'])])

    def test_invalid_data(self):
        data = {
            'username': 'testinva!',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())
        validator = next(v for v in User._meta.get_field('username').validators if v.code == 'invalid')
        self.assertEqual(form["username"].errors, [str(validator.message)])

    def test_password_verification(self):
        data = {
            'username': 'testinvalid',
            'password1': 'test123',
            'password2': 'test',
        }
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["password2"].errors,
                         [str(form.error_messages['password_mismatch'])])


class AuthFormTest(BaseFormTestCase):

    def test_valid_form(self):
        data = {
            'username': 'test',
            'password': 'test123',
        }
        form = AuthForm(data)
        self.assertTrue(form.is_valid())

    def test_required_username(self):
        data = {
            'password': '11test11'
        }
        form = AuthForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [Field.default_error_messages['required']])

    def test_required_password(self):
        data = {
            'username': 'test3'
        }
        form = AuthForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], [Field.default_error_messages['required']])


class CreateBlogFormTest(BaseFormTestCase):

    def test_valid_form(self):
        data = {
            'title': 'Test',
            'content': 'TestContent',
            'created_at': datetime.today().strftime('%d.%m.%Y'),
            'created_by': self.u1.id
        }
        form = CreateBlogForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'title': 'Test',
            'content': 'TestContent',
            'created_at': datetime.today().strftime('%d.%m.%Y'),
            'created_by': ''
        }
        form = CreateBlogForm(data)
        self.assertFalse(form.is_valid())
