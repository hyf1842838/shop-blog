
from datetime import timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.models import User, Articles, Category
from utils.functions import is_login


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # all()校验参数，如果列表中元素为空，则返回False
        if not all([username, password, password2]):
            msg = '请填写完整的参数'
            return render(request, 'register.html', {'msg': msg})
        if password != password2:
            msg = '密码不一致,请重新填写'
            return render(request, 'register.html', {'msg': msg})
        User.objects.create(username=username,
                             password=make_password(password))
        # 注册成功跳转到登录方法
        return HttpResponseRedirect(reverse('users:login'))


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        # 使用cookie+session形式实现登录
        username = request.POST.get('username')
        password = request.POST.get('userpwd')
        # all()校验参数，如果列表中元素为空，则返回False
        if not all([username, password]):
            msg = '请填写完整的参数'
            return render(request, 'login.html', {'msg': msg})
        # 校验是否能通过username和pasword找到user对象
        user = User.objects.filter(username=username).first()
        if user:
            # 校验密码
            if not check_password(password, user.password):
                msg = '密码错误'
                return render(request, 'login.html', {'msg': msg})
            else:
                # 向cookie中设置，向user_ticket表中设置
                request.session['user_id'] = user.id
                # 设置session数据在4天后过期过期时间
                request.session.set_expiry(timedelta(days=4))
                return HttpResponseRedirect(reverse('users:index'))
        else:
            msg = '用户名错误'
            return render(request, 'login.html', {'msg': msg, 'user': 'user'})

@is_login
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

@is_login
def logout(request):
    if request.method == 'GET':
        # 注销，删除session和cookie
        request.session.flush()
        # 获取session_key并实现删除,删除服务端
        # session_key = request.session.session_key
        # request.session.delete(session_key)

        return HttpResponseRedirect(reverse('users:login'))


def edit_article(request):
    """
    文章编辑方法
    """
    if request.method == 'GET':
        return render(request, 'edit.html')
    if request.method == 'POST':
        # 获取文章的标题和内容
        title = request.POST.get('title')
        content = request.POST.get('content')
        # 使用all()方法进行判断，如果文章标题和内容任何一个参数没有填写，则返回错误信息
        if not all([title, content]):
            msg = '请填写完整的参数'
            return render(request, 'edit.html', {'msg': msg})
        # 创建文章
        Articles.objects.create(title=title,
                               content=content)
        # 创建文章成功后，跳转到文章列表页面
        return HttpResponseRedirect(reverse('users:article'))


def article(request):
    """
    文章展示方法
    """
    if request.method == 'GET':
        # 获取所有的文章
        pag = int(request.GET.get('page', 1))
        articles = Articles.objects.all()
        pg = Paginator(articles, 2)
        my_pag = pg.page(pag)
        return render(request, 'article.html', {'articles': my_pag})



def add_category(request):
    if request.method == 'GET':
        return render(request, 'add-category.html')
    if request.method == 'POST':
        pass

def category(request):
    if request.method == 'GET':
        result = []
        categories = Category.objects.all()
        for categ in categories:
            articles = Articles.objects.filter(cat_id=categ.id)
            count = len(articles)
            result.append([categ, count])
        return render(request, 'category.html', {'result': result})

def loginlog(request):
    if request.method == 'GET':
        return render(request, 'loginlog.html')
    if request.method == 'POST':
        pass



def update_category(request):
    if request.method == 'GET':
        return render(request, 'update-category.html')
    if request.method == 'POST':
        pass

def add_art(request):
    if request.method == 'GET':
        return render(request, 'add-article.html')
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


def del_cat(request, id):
    if request.method == 'GET':
        Category.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('users:category'))