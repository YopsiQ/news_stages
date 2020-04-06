from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('<int:news_link>/', views.detail, name='detail'),
]
