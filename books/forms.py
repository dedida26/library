from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField

from .models import *


# Форма Регистрации пользователей содержит поля для ввода данных: логин пользователя, пароль,
# подтверждение пароля и поле Captcha, нужна форма для Регистрации на сайте

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()


# Форма Входа пользователей содержит поля для воода данных: логин, пароль и Captcha,
# нужна форма для входа в аккаунт на сайте

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()


# Форма Добавлении книг содержит класс Meta, который связан с моделью Book, отображает поля -
# "название книги", "автор", "дату публикации", для которых определены виджеты,
# нужна форма для добавления книг на сайт

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'published_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'author': forms.TextInput(attrs={'class': 'form-input'}),
            'published_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }


# Форма Редактирования книги содержит класс Meta, который связан с моделью Book, отображает поля -
# "название книги", "автор", "дату публикации", "резервацию"
# Метод __init__ настраивает виджет для поля published_date для более удобного ввода даты
# Метод save добавляет логику для управления резервированиями в зависимости от доступности книги
# def save(self, commit=True) Метод save сохраняет данные формы в базу данных
# book = super().save(commit=False): Вызывает метод save базового класса, чтобы сохранить данные формы,
# но с флагом commit=False, чтобы не сохранять объект сразу.
# if commit Проверяет, нужно ли сохранять объект в базе данных
# book.save(): Сохраняет объект в базе данных
# if not book.is_reserved Проверяет, доступна ли книга для бронирования.
# Reservation.objects.filter(book=book).delete() Если книга недоступна, удаляет все резервирования для этой книги

class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'published_date', 'is_reserved')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['published_date'].widget.attrs['type'] = 'date'

    def save(self, commit=True):
        book = super().save(commit=False)
        if commit:
            book.save()

        if not book.is_reserved:
            Reservation.objects.filter(book=book).delete()

        return book


# Форма Резервирования книги содержит класс Meta, который связан с моделью Reservation,
# отображает одно поле reservation_date и виджет для его отображения

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_date']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }


# Форма Просмотра зарезервированных книг
# self.reserved_books = Book.objects.filter(is_reserved=True) Запрашивает из базы данных все книги,
# у которых атрибут is_reserved равен True (т.е. доступные книги). Результаты запроса сохраняются в
# свойство self.reserved_books.
# self.fields['reserved_book'] = forms.ChoiceField(...) Создает поле формы с именем reserved_book,
# которое представляет собой поле выбора
# choices=[(book.id, book.name) for book in self.reserved_books]: Устанавливает список вариантов выбора для этого поля.

class ViewReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reserved_books = Book.objects.filter(is_reserved=True)
        self.fields['reserved_book'] = forms.ChoiceField(
            choices=[(book.id, book.name) for book in self.reserved_books],
            label='Зарезервированная книга',
            required=True,
        )
