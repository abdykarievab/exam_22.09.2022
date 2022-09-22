from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, \
    get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .models import News, Comment, Status, NewsStatus, CommentStatus
from .serializers import NewsSerializer, CommentSerializer
from account.models import Author
from .permissions import NewsPermission, CommentPermission


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (NewsPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)


class CommentView:
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class CommentCreateListView(CommentView, ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author, news=News.objects.get(id=self.kwargs['news_id']))

    def get_queryset(self):
        return self.queryset.filter(news=self.kwargs['news_id'])


class CommentRetrieveUpdateDestroyView(CommentView, RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)




