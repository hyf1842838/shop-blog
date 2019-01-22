from django.urls import path

from user import views

urlpatterns = [
    # 注册
    path('register/', views.register, name='register'),
    # 登陆
    path('login/', views.login, name='login'),
    # 退出
    path('logout/', views.logout, name='logout'),
    # 地址编辑
    path('user_center_site/', views.user_center_site, name='user_center_site'),
    # 个人中心
    path('user_info/', views.user_info, name='user_info'),
]