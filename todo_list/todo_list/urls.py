"""
URL configuration for todo_list project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path, re_path
from rest_framework import routers
from todo import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'folders', views.FolderViewSet)
router.register(r'pages', views.PageViewSet)
router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v3/todo-auth/', include('rest_framework.urls')),
    path('api/v3/', include(router.urls)),
    path('api/v3/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v3/pages/<int:pk>/', views.PageViewSet.as_view({'get': 'retrieve'}), name='page-detail'),
    path('api/v3/folders/<int:pk>/', views.FolderViewSet.as_view({'get': 'retrieve'}), name='folder-detail'),
]
