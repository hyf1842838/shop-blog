
from django.urls import path

from users import views

urlpatterns = [
    # 注册
    path(r'register/', views.register, name='register'),
    # 登录
    path(r'login/', views.login, name='login'),
    # 首页
    path(r'index/', views.index, name='index'),
    # 注销
    path(r'logout/', views.logout, name='logout'),
    # 编辑文章
    path(r'edit_article/', views.edit_article, name='edit_article'),
    # 文章列表
    path(r'article/', views.article, name='article'),
    # 添加文章
    path('add_art/', views.add_art, name='add_article'),
    # 添加栏目
    path('add_cat/', views.add_category, name='add_category'),
    # 栏目
    path('category/', views.category, name='category'),
    # 查看记录
    path('loginlog/', views.loginlog, name='loginlog'),
    # 修改文章
    path('upd_art/', views.upd_art, name='update_article'),
    # 修改栏目
    path('upd_cat/', views.update_category, name='update_category'),
    # 删除栏目
    path('del_cat/<int:id>/', views.del_cat, name='del_cat'),
]

