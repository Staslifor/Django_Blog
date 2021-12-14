from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_blog',
                                verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Данные пользователя'
        verbose_name_plural = 'Данные пользователя'
        db_table = 'profile'


class BlogModel(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='creator')

    def __str__(self):
        return self.title

    def content_slice(self):
        return self.content[:100]

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        db_table = 'blogs'
        ordering = ['-created_at']


class File(models.Model):
    file = models.FileField(upload_to='images/%Y/%m/%d', blank=True, verbose_name="Файлы")
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='files')
