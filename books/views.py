from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView, UpdateView
from .forms import *


# Класс Регистрации, будет использовать Формы регистрации для обработки ввода данных, используется шаблон register,
# после успешной регистрации происходит переход на главную страницу, с авторизированным профилем

class RegisterUser(CreateView):
    form_class = RegistrationForm
    template_name = 'book/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


# Класс Входа, будет использовать Форму входа для обработки ввода данных, используется шаблон login,
# после успешного входа происходит переход на главную

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'book/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


# Функция Выхода с аккаунта, после нее переходит на Вход в аккаунт

def logout_user(request):
    logout(request)
    return redirect('login')


# Класс Главная страница, отображает список объектов модели Book, используется шаблон index,
# контекстное имя для обращения к списку объектов Book в шаблоне - books

class BookHome(ListView):
    model = Book
    template_name = 'book/index.html'
    context_object_name = 'books'


# Класс Добавление книги, будет использовать Форму Добавления книг для обработки ввода данных,
# используется шаблон addbook, после успошного добавления происходит переход на главную

class AddBook(CreateView):
    form_class = AddBookForm
    template_name = 'book/addbook.html'
    success_url = reverse_lazy('home')


# Класс Изменения книги, отображает список объектов модели Book,
# используется шаблон editbook, после успошного изменения происходит переход на главную

class EditBook(UpdateView):
    model = Book
    form_class = EditBookForm
    template_name = 'book/editbook.html'
    success_url = reverse_lazy('home')


# Класс Резервирования книги, будет использовать Форму Резервирования книги для обработки ввода данных,
# используется шаблон reservation, после успошного добавления происходит переход на главную,
# book_pk = self.kwargs['pk'] Извлекает идентификатор книги (PK) из URL, используя self.kwargs
# book = Book.objects.get(pk=book_pk) Запрашивает объект Book из базы данных по его идентификатору
# user = self.request.user Получает текущего авторизованного пользователя из запроса
# reservation = form.save(commit=False) Создает объект Reservation,
# но не сохраняет его в базу данных сразу (используя commit=False)
# reservation.book = book Привязывает объект book к резервированию.
# reservation.user = user Привязывает текущего пользователя к резервированию.
# reservation.save() Сохраняет объект reservation в базу данных.
# book.is_reserved = True Устанавливает флаг is_reserved в объекте book в значение True,
# указывая, что книга зарезервирована.
# book.save() Сохраняет изменения в объекте book в базу данных.
# return super().form_valid(form): Вызывает метод form_valid родительского класса,
# чтобы продолжить обработку формы (например, перенаправление на success_url).

class ReservationBook(FormView):
    form_class = ReservationForm
    template_name = 'book/reservation.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        book_pk = self.kwargs['pk']
        book = Book.objects.get(pk=book_pk)
        user = self.request.user
        reservation = form.save(commit=False)
        reservation.book = book
        reservation.user = user
        reservation.save()
        book.is_reserved = True
        book.save()
        return super().form_valid(form)


# Класс Просмотра Зарезервированных книг отображает список объектов модели Reservation,
# используется шаблон reservationbooks, контекстное имя для обращения к списку объектов
# Reserved в шаблоне - reservations
# super().get_queryset() Вызывает метод get_queryset родительского класса ListView,
# чтобы получить стандартный запрос для всех объектов Reservation
# .select_related('book') Добавляет к запросу select_related для поля book,
# чтобы извлечь данные о книге непосредственно при запросе резервирования. Это улучшает производительность,
# так как не требуется отдельных запросов к базе данных для получения данных о книге для каждого резервирования
# .order_by('reservation_date') Сортирует запрошенные данные по дате резервирования (поле reservation_date)
class ViewReservationBook(ListView):
    model = Reservation
    template_name = 'book/reservationbooks.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return super().get_queryset().select_related('book').order_by('reservation_date')
