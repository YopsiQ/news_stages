from django.urls import path

from . import views

urlpatterns = [
    path('<int:news_link>/', views.detail, name='detail'),
]
