import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from users.models import Articles, Category

logger = logging.getLogger(__name__)

# def index(request):
#     if request.method == 'GET':
#         print('index views')
#         1/0
#         return HttpResponse('我是index方法')
        # 1/0
        # return render(request, 'index.html')

#
# def index(request):
#     print('index views')
#
#     def index_render():
#         return render(request, 'index.html')
#
#     rep = HttpResponse()
#     rep.render = index_render
#     return rep


def index(request):
    """
    index方法中添加记录日志
    """
    if request.method == 'GET':
        logger.info('index方法')
        return HttpResponse('我是首页，我需要有修改用户名的权限才能访问')


def add_art(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, 'add-article.html', {'categorys': categories})
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        keywords = request.POST.get('keywords')
        describ = request.POST.get('describe')
        category = request.POST.get('category')
        tags = request.POST.get('tags')
        titlepic = request.POST.get('titlepic')
        visibility = request.POST.get('visibility')
        article = Articles.objects.filter(content=content).first()
        if not article:
            Articles.objects.create(title=title, content=content, keywords=keywords, describ=describ, category=category,
                                   tags=tags, titlepic=titlepic, visibility=visibility)

            return HttpResponseRedirect(reverse('users:article'))




def del_art(request, id):
    if request.method == 'GET':
        Articles.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('users:article'))

def upd_art(request, id):
    if request.method == 'GET':
        return render(request, 'update-article.html')
    if request.method == 'POST':
        article = Articles.objects.filter(pk=id).first()
        if article:
            article.title = request.POST.get('title')
            article.content = request.POST.get('content')
            article.keywords = request.POST.get('keywords')
            article.describ = request.POST.get('describe')
            article.category = request.POST.get('category')
            article.tags = request.POST.get('tags')
            article.titlepic = request.POST.get('titlepic')
            article.visibility = request.POST.get('visibility')
            article.save()
            return HttpResponseRedirect(reverse('users:article'))


