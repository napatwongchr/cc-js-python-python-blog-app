from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connections

from blogs.models import Post

@csrf_exempt
def post_list(request):
  if request.method == "GET":
    posts = Post.objects.all()
    data = list(posts.values())

    response_data = {}
    response_data['data'] = data
    response = JsonResponse(response_data)
    response.status_code = 200
    return response


  if request.method == "POST":
    data = json.loads(request.body)

    post = Post(
      title=data["title"],
      content=data["content"]
    )

    post.save()

    response = JsonResponse({"message": "created post successfully" })
    response.status_code = 201

    return response

@csrf_exempt
def single_post_detail(request, post_id):
  if request.method == "GET":
    post = Post.objects.filter(id=post_id)
    data = post.values()[0]

    response_data = {}
    response_data["data"] = data

    response = JsonResponse(response_data)
    response.status_code = 200
    return response

  if request.method == "PUT":
    request_data = json.loads(request.body)

    post = Post.objects.filter(id=post_id)[0]
    post.title = request_data["title"]
    post.content = request_data["content"]
    post.save()
    
    response = JsonResponse({ "message": "updated post successfully." })
    response.status_code = 200
    return response

  if request.method == "DELETE":
    post = Post.objects.filter(id=post_id)[0]
    post.delete()
    
    response = JsonResponse({ "message": "deleted post successfully" })
    response.status_code = 200
    return response

  response = JsonResponse({ "data": { } })
  response.status_code = 404
  return response