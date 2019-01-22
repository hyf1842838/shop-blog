import random

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from goods.models import GoodsCategory, Goods


def index(request):
    # 如果访问首页，返回渲染的首页index.html
    if request.method == 'GET':
        # 组装结果的对象：包含分类，该分类的前四个商品信息
        # 方式一：object -->[GoodsCategory object,[Goods objects1,Goods objects2...]]
        # 方式二：object -->{'category_name':[Goods object1, Goods objects2...]}
        categorys = GoodsCategory.objects.all()
        result = []
        for category in categorys:
            goods = category.goods_set.all()[:4]
            data = [category, goods]
            result.append(data)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request, 'index.html', {'result': result, 'category_type': category_type})


def detail(request, id):
    if request.method == 'GET':
        good = Goods.objects.filter(pk=id).first()
        return render(request, 'detail.html', {'good': good})


def list_goods(request, cat_id):
    if request.method == 'GET':
        all_goods = Goods.objects.filter(category=cat_id)
        return render(request, 'list.html', {'all_goods': all_goods})