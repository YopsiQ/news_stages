from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adding_page/', views.adding_page, name='adding_page'),
    path('create/', views.create, name='create'),
    path('<str:news_link>/', views.detail, name='detail'),
]
