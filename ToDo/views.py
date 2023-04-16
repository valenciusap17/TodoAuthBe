from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

import jwt
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
# Create your views here.

def index(request):
    return render()

@csrf_exempt
def show_json(request):
    message_per_category = ToDoMessage.objects.all()
    return HttpResponse(serializers.serialize("json", message_per_category), content_type="application/json")

@csrf_exempt
def post_data(request):
    if request.method == "POST":
        print(request.body)
        body = json.loads(request.body)
        print(body.get("message_data"))
        message_data = body.get("message_data")
        date_data = body.get("date_data")
        category = body.get("category")

        chosenCategory = Category.objects.get(pk=category)
        print(chosenCategory.category_data)

        new_messsage = ToDoMessage(message_data = message_data, date_data=date_data, category=chosenCategory)
        print(new_messsage.category.category_data)
        new_messsage.save()
        return HttpResponse()
    
@csrf_exempt
def delete_data(request):
    if request.method == "POST":
        print(request.body)
        body = json.loads(request.body)
        chosenData = ToDoMessage.objects.get(pk=body["pk"])
        chosenData.delete()
        return HttpResponse()
    
@csrf_exempt
def edit_data(request):
    if request.method == "POST":
        body = json.loads(request.body)
        chosenData = ToDoMessage.objects.get(pk=body["pk"])
        chosenData.message_data = body.get("newMessageData")
        chosenData.save()
        return HttpResponse()
    
@csrf_exempt
def finished_data(request):
    if request.method == "POST":
        body = json.loads(request.body)
        chosenData = ToDoMessage.objects.get(pk=body["pk"])
        chosenData.is_finished = not chosenData.is_finished
        chosenData.save()
        return HttpResponse()
    
def login_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        token = generate_jwt_token(user.id)
        return JsonResponse({'token': token.decode('utf-8')})
    else:
        return JsonResponse({'error': 'Invalid credentials'})
    
def generate_jwt_token(user_id):
    token_expiry_time = datetime + timedelta(minutes=30)

def register(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body.get('email')
        password = body.get('password')
        username = body.get('username')

        try:
            user = User.objects.create_user(email=email,username=username , password=password)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    
        token = generate_jwt_token(user.id)
        return JsonResponse({'token': token.decode('utf-8')})
    else :
        return JsonResponse({'error': "Invalid request method"}, status=405)
    
@csrf_exempt    
def post_category(request):
    if request.method == "POST":
        body = json.loads(request.body)
        color = body.get('color')
        categoryData = body.get('category_data')
        new_category = Category(color=color, category_data=categoryData)
        new_category.save()
        return HttpResponse()

@csrf_exempt    
def category_json(request):
    category = Category.objects.all()
    return HttpResponse(serializers.serialize("json", category), content_type="application/json")