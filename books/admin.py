from django.contrib import admin

from .models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'published_date', 'is_reserved')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'author')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_book_display', 'reservation_date')
    list_display_links = ('id', 'user')

    def get_book_display(self, obj):
        return obj.book.title

    get_book_display.short_description = 'Название книги'


admin.site.register(Book, BookAdmin)
admin.site.register(Reservation, ReservationAdmin)
