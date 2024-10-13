from django.shortcuts import render, redirect
from news.models import Category, CategoryForm, News, NewsForm, User
from rest_framework import viewsets
from news.serializers import CategorySerializer, NewsSerializer, UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


def index(request):
    context = {"news_list": News.objects.all()}
    return render(request, 'home.html', context)


def news(request, id):
    context = {"news_details": News.objects.get(id=id)}
    return render(request, 'news_details.html', context)


def new_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home-page')
    else:
        form = CategoryForm()
        context = {'form': form}
        return render(request, 'categories_form.html', context)


def new_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home-page')
    else:
        form = NewsForm()
        users = User.objects.all()
        categories = Category.objects.all()
        return render(request, 'news_form.html',
                      {'form': form, 'users': users, 'categories': categories})
