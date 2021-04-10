from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connections

@csrf_exempt
def post_list(request):
  if request.method == "GET":
    with connections['default'].cursor() as cursor:
      cursor.execute("SELECT * FROM blogs_post")
      columns = [col[0] for col in cursor.description]
      data = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
      ]

    response_data = {}
    response_data['data'] = data
    response = JsonResponse(response_data)
    response.status_code = 200
    return response


  if request.method == "POST":
    data = json.loads(request.body)

    with connections['default'].cursor() as cursor:
     cursor.execute("INSERT INTO blogs_post (title, content) VALUES (%s, %s)", [ data["title"], data["content"] ])

    response = JsonResponse({"message": "created post successfully" })
    response.status_code = 201

    return response

@csrf_exempt
def single_post_detail(request, post_id):
  if request.method == "GET":
    with connections["default"].cursor() as cursor:
      cursor.execute("SELECT * FROM blogs_post WHERE id = %s", [post_id])

      columns = [col[0] for col in cursor.description]

      data = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
      ]

    response_data = {}
    response_data["data"] = data

    response = JsonResponse(response_data)
    response.status_code = 200
    return response

  if request.method == "PUT":
    request_data = json.loads(request.body)

    with connections['default'].cursor() as cursor:
      query = "UPDATE blogs_post SET title=%s, content=%s WHERE id=%s"
      cursor.execute(
        query, 
        [request_data["title"], request_data["content"], post_id]
      )
    
    response = JsonResponse({ "message": "updated post successfully." })
    response.status_code = 200
    return response

  if request.method == "DELETE":
    with connections['default'].cursor() as cursor:
      cursor.execute("DELETE FROM blogs_post WHERE id = %s", [post_id])
    
    response = JsonResponse({ "message": "deleted post successfully" })
    response.status_code = 200
    return response

  response = JsonResponse({ "data": { } })
  response.status_code = 404
  return response