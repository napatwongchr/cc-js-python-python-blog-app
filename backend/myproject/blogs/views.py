from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

posts = {
  "data": [
    {
      "id": "1",
      "title": "Post 1",
      "content": "This is post 1 content"
    }
  ]
}

@csrf_exempt
def post_list(request):
  if request.method == "GET":
    response = JsonResponse(posts)
    response.status_code = 200
    return response
  
  if request.method == "POST":
    data = json.loads(request.body)
    posts["data"].append({ "id": "2", "title": data["title"], "content": data["content"] })
    
    response = JsonResponse({ "message": "created post successfully" })
    response.status_code = 201
    
    return response

@csrf_exempt
def single_post_detail(request, post_id):
  if request.method == "GET":
    for post in posts["data"]:
      if post["id"] == post_id:
        response = JsonResponse({ "data": post })
        response.status_code = 200
        return response

  if request.method == "PUT":
    request_data = json.loads(request.body)

    for post_item in posts["data"]:
      if post_item["id"] == post_id:
        post_item["title"] = request_data["title"]
        post_item["content"] = request_data["content"]

        response = JsonResponse({ "message": "updated post successfully" })
        response.status_code = 200
        return response
  
  if request.method == "DELETE":
    new_posts = []

    for post_item in posts["data"]:
      if post_item["id"] != post_id:
        new_posts.append(post_item)

    posts["data"] = new_posts
    
    response = JsonResponse({ "message": "deleted post successfully" })
    response.status_code = 200
    return response

  response = JsonResponse({ "data": { } })
  response.status_code = 404
  return response