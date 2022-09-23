from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('news', views.NewsViewSet, basename='news')
router.register('statuses', views.StatusViewSet, basename='statuses')

urlpatterns = [
    path('', include(router.urls)),
    path('news/<int:news_id>/comments/', views.CommentCreateListView.as_view()),
    path('news/<int:news_id>/comments/<int:pk>/',
         views.CommentRetrieveUpdateDestroyView.as_view()),
    path('news/<int:news_id>/<str:slug>/', views.NewsPostStatus.as_view()),
    path('news/<int:news_id>/comments/<int:comment_id>/<str:slug>/', views.CommentPostStatus.as_view()),
]
