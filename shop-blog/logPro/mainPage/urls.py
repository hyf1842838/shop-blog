from django.urls import path

from mainPage import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('gbook/', views.gbook, name='gbook'),
    path('infopic/', views.infopic, name='infopic'),
    path('info/', views.info, name='info'),
    path('list/', views.list, name='list'),
    path('share/', views.share, name='share'),
    path('look/<int:id>/', views.look, name='look'),
]