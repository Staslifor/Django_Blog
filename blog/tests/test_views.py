import csv

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from ..models import BlogModel
from datetime import datetime
import os

USER_EMAIL = 'test@test.com'
OLD_PASSWORD = 'testpassword'


class BaseTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='11test11')
        self.user.save()
        self._register_data = {
            'username': 'testuser',
            'first_name': 'firstnametest',
            'last_name': 'lastnametest',
            'password1': '11test11',
            'password2': '11test11',
            'email': 'tesyemail@test.com',
        }
        self._invalid_register_data = {
            'username': '',
            'first_name': 'firstnametest',
            'last_name': 'lastnametest',
            'password1': '11test11',
            'password2': '11test11',
            'email': 'tesyemail@test.com',
        }
        self._short_password = {
            'username': 'testuser',
            'first_name': 'firstnametest',
            'last_name': 'lastnametest',
            'password1': '11te',
            'password2': '11te',
            'email': 'tesyemail@test.com',
        }
        self._data_for_blog = {
            'title': 'Testttle',
            'content': 'Testcontent',
            'created_by': self.user.id
        }
        self._data_for_blog_without_title = {
            'title': '',
            'content': 'Testcontent',
            'created_by': self.user.id
        }
        self._data_for_blog_without_content = {
            'title': 'Testttle',
            'content': '',
            'created_by': self.user.id
        }

    @classmethod
    def generate_file(cls):
        file_name = 'test.csv'
        try:
            file_for_load = open(file_name, 'w', newline="")
            wr = csv.writer(file_for_load, delimiter=';')
            date = datetime.today()
            wr.writerow(('TestTitle1', 'TestContent1', date.strftime('%d.%m.%Y')))
            wr.writerow(('TestTitle2', 'TestContent2', date.strftime('%d.%m.%Y')))
        finally:
            file_for_load.close()
            return file_name

    @classmethod
    def generate_uncorrect_file(cls):
        name = 'test.csv'
        try:
            file_for_load = open(name, 'w', newline="")
            wr = csv.writer(file_for_load, delimiter=';')
            wr.writerow(('TestTitle1', 'TestContent1'))
            wr.writerow(('TestTitle2', 'TestContent2'))
        finally:
            file_for_load.close()
            return name

    def tearDown(self):
        self.user.delete()
        os.remove(os.path.abspath(self.generate_file()))
        os.remove(os.path.abspath(self.generate_uncorrect_file()))


class RegisterViewTest(BaseTestCase):

    def test_register_view_url_exists_and_describe_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_view_uses_correct_template(self):  # TODO такие тесты не нужны
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/register.html')

    def test_can_register_user(self):
        self.client.post('/register/', self._register_data)
        try:
            user = User.objects.get(username=self._register_data['username'])
        except User.DoesNotExist:
            user = None
        self.assertIsInstance(user, User)

    def test_invalid_register_data(self):
        self.client.post('/register/', self._invalid_register_data)
        try:
            user = User.objects.get(username=self._register_data['username'])
        except User.DoesNotExist:
            user = None
        self.assertNotIsInstance(user, User)

    def test_short_password(self):
        self.client.post('/register/', self._short_password)
        try:
            user = User.objects.get(username=self._register_data['username'])
        except User.DoesNotExist:
            user = None
        self.assertNotIsInstance(user, User)


class LoginViewTest(BaseTestCase):

    def test_login_view_url_exists_and_describe_location(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_correct_template(self):  # TODO Аналогично предыдущему
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/login.html')

    def test_login_success(self):
        response = self.client.post('/login/', {'username': 'test', "password": '11test11'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_wrong_username(self):
        response = self.client.post('/login/', {'username': 'wrong', "password": '11test11'}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_wrong_password(self):
        response = self.client.post('/login/', {'username': 'wrong', "password": 'wrong'}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


class CreateBlogViewTest(BaseTestCase):

    def test_creation_view_url_exists_and_describe_location(self):
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_creation_view_uses_correct_template(self):  # TODO Аналогично предыдущему
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/create_blog.html')

    def test_create_blog(self):
        response = self.client.post('/create/', self._data_for_blog)
        created_blog = BlogModel.objects.count()
        self.assertRedirects(response, expected_url='/', status_code=302, target_status_code=200)
        self.assertEqual(created_blog, 1)

    def test_fail_blog_creation_without_title(self):
        response = self.client.post('/create/', self._data_for_blog_without_title)
        created_blog = BlogModel.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(created_blog, 0)

    def test_fail_blog_creation_without_content(self):
        response = self.client.post('/create/', self._data_for_blog_without_content)
        created_blog = BlogModel.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(created_blog, 0)


class LoadBlogView(BaseTestCase):

    def test_load_blog_view_url_exists_and_describe_location(self):
        response = self.client.get('/load/')
        self.assertEqual(response.status_code, 200)

    def test_load_blog_view_uses_correct_template(self):
        response = self.client.get(reverse('load_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/load_csv.html')

    def test_load_file(self):
        self.client.post('/login/', {'username': 'test', "password": '11test11'}, follow=True)
        file_for_load = self.generate_file()
        with open(file_for_load, 'r') as f:
            response = self.client.post('/load/', {'file': f})
        created_blog = BlogModel.objects.count()
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, expected_url='/', status_code=302, target_status_code=200)
        self.assertEqual(created_blog, 2)

    def test_unload_file(self):
        self.client.post('/login/', {'username': 'test', "password": '11test11'}, follow=True)
        file_for_load = self.generate_uncorrect_file()
        with open(file_for_load, 'r') as f:
            try:
                self.client.post('/load/', {'file': f})
            except IndexError:
                created_blog = BlogModel.objects.count()
        self.assertEqual(created_blog, 0)
