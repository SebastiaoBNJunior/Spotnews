from django import forms
from django.db import models
from news.validators import validate_title


class Category(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    role = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(max_length=200, blank=False, null=False)
    password = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        validators=[validate_title]
        )
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    created_at = models.DateField()
    image = models.ImageField(upload_to='img/', blank=True, null=True)

    def __str__(self):
        return self.title


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'title',
            'content',
            'author',
            'categories',
            'created_at',
            'image'
            ]
