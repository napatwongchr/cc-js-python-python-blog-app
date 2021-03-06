from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connections

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from blogs.serializers import CommentSerializer, PostSerializer
from blogs.models import Post, Comment

@api_view(['GET'])
def comment_list(request, post_id):
  if request.method == "GET":
    comments = Comment.objects.filter(post_id=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response({ "data": serializer.data })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list(request):
  if request.method == "GET":
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response({ "data": serializer.data })

  if request.method == "POST":
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({ "message": "created post successfully" }, status=status.HTTP_201_CREATED)
    
    return Response({ "message": "created post failed", "errors": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def single_post_detail(request, post_id):
  post = Post.objects.filter(id=post_id)[0]

  if not len(post):
    return Response({ "message": "post not found" }, status=status.HTTP_404_NOT_FOUND)

  if request.method == "GET":
    serializer = PostSerializer(post)
    return Response({ "data": serializer.data })

  if request.method == "PUT":
    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({ "message": "updated post succesfully "})
    return Response({ "message": "updated post failed" }, status=status.HTTP_400_BAD_REQUEST)

  if request.method == "DELETE":
    post.delete()
    return Response({ "message": "deleted post successfully" })