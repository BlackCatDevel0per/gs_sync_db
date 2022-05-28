from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('usd/', views.index_usd, name='usd'),
    path('rub/', views.index_rub, name='rub'),
]