from django.urls import path, include
from .views import index, new_category, new_news, news
from rest_framework import routers
from .views import CategoryViewSet, UserViewSet, NewsViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'users', UserViewSet)
router.register(r'news', NewsViewSet)

urlpatterns = [
  path('', index, name='home-page'),
  path('news/<int:id>/', news, name='news-details-page'),
  path('categories/', new_category, name='categories-form'),
  path('news/', new_news, name='news-form'),
  path('api/', include(router.urls)),
]
