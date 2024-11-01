from django.urls import path
from .views import *

urlpatterns = [
    path('', BookHome.as_view(), name='home'),
    path('addbook/', AddBook.as_view(), name='add_book'),
    path('editbook/<int:pk>/', EditBook.as_view(), name='edit_book'),
    path('reservation/<int:pk>/', ReservationBook.as_view(), name='reservation_book'),
    path('viewreservation/', ViewReservationBook.as_view(), name='viewreservation_book'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]
