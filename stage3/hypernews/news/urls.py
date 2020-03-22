from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:news_link>/', views.detail, name='detail'),
]
