
from django.urls import path

from app import views


urlpatterns = [
    path(r'index/', views.index, name='index'),
    path(r'add_art/', views.add_art, name='add_art'),
    path('del_art/<int:id>/', views.del_art, name='del_art'),
    path('upd_art/<int:id>/', views.upd_art, name='upd_art'),
]



