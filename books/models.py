from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# Модель "Книг" содержит: название, автора, дату публикации, сведения о резервации,
# нужна модель для создания записи в БД

class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название книги')
    author = models.CharField(max_length=100, verbose_name='Автор книги')
    published_date = models.DateField(verbose_name='Дата публикации')
    is_reserved = models.BooleanField(default=False, verbose_name='Зарезервировано')


# Модель "Резерва" содержит: внешний ключ на встроенную модель в Django "User",
# внешний ключ на модель "Book" и дату резервирвоания книги,
# нужна модель для создания записи в БД

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reservation_date = models.DateField(default=datetime.now)
