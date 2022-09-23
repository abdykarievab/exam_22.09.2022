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
from .serializers import NewsSerializer, CommentSerializer, StatusSerializer
from account.models import Author
from .permissions import NewsPermission, CommentPermission


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAdminUser, ]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

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


class NewsPostStatus(APIView):
    model = NewsStatus
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, news_id, slug):
        news = get_object_or_404(News, id=news_id)
        status = get_object_or_404(Status, slug=slug)
        try:
            self.model.objects.create(
                news=news,
                author=request.user.author,
                status=status
            )
        except IntegrityError:
            return Response({'error': 'You already added status'})
        else:
            return Response({'message': 'Status added'})


class CommentPostStatus(APIView):
    model = CommentStatus
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, news_id, comment_id, slug):
        comment = get_object_or_404(Comment, id=comment_id, news__id=news_id)
        status = get_object_or_404(Status, slug=slug)
        try:
            self.model.objects.create(
                comment=comment,
                author=request.user.author,
                status=status
            )
        except IntegrityError:
            return Response({'error': 'You already added status'})
        else:
            return Response({'message': 'Status added'})


