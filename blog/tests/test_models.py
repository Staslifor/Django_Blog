from django.test import TestCase
from ..models import Profile, BlogModel, File
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class BaseModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseModelTestCase, cls).setUpClass()
        cls.user = User.objects.create_user(username='test2', password='11test11')
        cls.blog = BlogModel.objects.create(
            title='Test',
            content='TestContent',
            created_at=datetime.today().strftime('%d.%m.%Y'),
            created_by=cls.user
        )

        cls.blog_id1 = BlogModel.objects.get(id=1)
        cls.title = cls.blog_id1._meta.get_field('title')
        cls.content = cls.blog_id1._meta.get_field('content')
        cls.created_at = cls.blog_id1._meta.get_field('created_at')
        cls.updated_at = cls.blog_id1._meta.get_field('updated_at')
        cls.created_by = cls.blog_id1._meta.get_field('created_by')

        cls.file = File.objects.create(blog=cls.blog)
        cls.user_profile = Profile.objects.create(user=cls.blog.created_by)
        cls.profile_user = cls.user_profile._meta.get_field('user')


class BlogModelTest(BaseModelTestCase):

    def test_fields_instance_string(self):
        self.assertIsInstance(self.blog.title, str)
        self.assertIsInstance(self.blog.content, str)

    def test_field_instance_CharField(self):
        self.assertIsInstance(self.title, models.CharField)

    def test_field_instance_TextField(self):
        self.assertIsInstance(self.content, models.TextField)

    def test_field_instance_date(self):
        self.assertIsInstance(self.blog.created_at, datetime)

    def test_field_instance_User(self):
        self.assertIsInstance(self.blog.created_by, User)

    def test_field_instance_ForeignKey(self):
        self.assertIsInstance(self.created_by, models.ForeignKey)

    def test_max_length_title(self):
        blog = BlogModel.objects.get(id=1)
        max_length = blog._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_verbose_name(self):
        self.assertEquals(self.title.verbose_name, 'Заголовок')
        self.assertEquals(self.content.verbose_name, 'Контент')
        self.assertEquals(self.created_at.verbose_name, 'Дата публикации')
        self.assertEquals(self.updated_at.verbose_name, 'Дата обновления')
        self.assertEquals(self.created_by.verbose_name, 'Автор')

    def test__blog_verbose_name_(self):
        blog = self.blog._meta.verbose_name
        self.assertEqual(str(blog), 'Блог')

    def test__blog_verbose_name_plural(self):
        blog = self.blog._meta.verbose_name_plural
        self.assertEqual(str(blog), 'Блоги')

    def test__blog_db_table(self):
        blog = self.blog._meta.db_table
        self.assertEqual(str(blog), 'blogs')

    def test__blog_ordering(self):
        blog = self.blog._meta.ordering
        self.assertEqual(blog, ['-created_at'])


class FileTestModel(BaseModelTestCase):

    def test_file_verbose_name(self):
        file_meta = self.file._meta.get_field('file')
        self.assertEqual(str(file_meta.verbose_name), 'Файлы')

    def test_fields_instance_FileField(self):
        file_meta = self.file._meta.get_field('file')
        self.assertIsInstance(file_meta, models.FileField)

    def test_fields_instance_ForeignKey(self):
        file_meta = self.file._meta.get_field('blog')
        self.assertIsInstance(file_meta, models.ForeignKey)

    def test_field_instance_blog_BlogModel(self):
        self.assertIsInstance(self.file.blog, BlogModel)


class ProfileTestModel(BaseModelTestCase):

    def test_user_filed_instance(self):
        self.assertIsInstance(self.profile_user, models.OneToOneField)
        self.assertIsInstance(self.user_profile.user, User)

    def test_user_filed_verbose_name(self):
        self.assertEquals(self.profile_user.verbose_name, 'Пользователь')

    def test_user_meta(self):
        user_profile_meta = self.user_profile._meta
        self.assertEqual(user_profile_meta.verbose_name_plural, 'Данные пользователя')
        self.assertEqual(user_profile_meta.verbose_name, 'Данные пользователя')
        self.assertEqual(user_profile_meta.db_table, 'profile')
