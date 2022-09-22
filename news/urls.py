from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('', views.NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:news_id>/comments/', views.CommentCreateListView.as_view()),
    path('<int:news_id>/comments/<int:pk>/',
         views.CommentRetrieveUpdateDestroyView.as_view()),

]
