from django.urls import path, include

from goods import views

urlpatterns = [
    # 主页
    path('index/', views.index, name='index'),
    # 详情页
    path('detail/<int:id>/', views.detail, name='detail'),
    # 查看商品类别
    path('list_goods/<int:cat_id>/', views.list_goods, name='list_goods'),
]