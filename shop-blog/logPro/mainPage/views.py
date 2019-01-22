from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from django.urls import reverse

from mainPage.models import Articles


def index(request):
    if request.method == 'GET':
        articles = Articles.objects.all()
        return render(request, 'index.html', {'articles': articles})


def about(request):
    return render(request, 'about.html')


def gbook(request):
    return render(request, 'gbook.html')


def infopic(request):
    return render(request, 'infopic.html')


def info(request):
    if request.method == 'GET':
        articles = Articles.objects.all()
        return render(request, 'info.html', {'articles': articles})


def list(request):
    if request.method == 'GET':
        pag = int(request.GET.get('page', 1))
        articles = Articles.objects.all()
        pg = Paginator(articles, 3)
        my_pag = pg.page(pag)
        return render(request, 'list.html', {'articles': my_pag})


def share(request):
    if request.method == 'GET':
        pag = int(request.GET.get('page', 1))
        arts = Articles.objects.all()
        pg = Paginator(arts, 3)
        my_pag = pg.page(pag)
        return render(request, 'share.html', {'art': my_pag})



def look(request, id):
    if request.method == 'GET':
        art = Articles.objects.filter(pk=id).first()
        return render(request, 'info.html', {'art': art})