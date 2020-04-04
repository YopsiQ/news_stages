from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:news_link>/', views.detail, name='detail'),
]
