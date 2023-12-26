from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

# Create your views here.


@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response({"detail": "Not Found"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({"token": token.key})


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print("masuk kan")
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def testToken(request):
    return Response("passed for {}".format(request.user.email))


@login_required
@csrf_exempt
@require_http_methods(["GET"])
def show_json(request):
    message_per_category = ToDoMessage.objects.filter(user=request.user)
    return HttpResponse(
        serializers.serialize("json", message_per_category),
        content_type="application/json",
    )


@login_required
@csrf_exempt
def post_data(request):
    if request.method == "POST":
        print(request.body)
        body = json.loads(request.body)
        print(body.get("message_data"))
        message_data = body.get("message_data")
        date_data = body.get("date_data")
        category = body.get("category")

        try:
            chosenCategory = Category.objects.get(pk=category)
            new_messsage = ToDoMessage(
                user=request.user,
                message_data=message_data,
                date_data=date_data,
                category=chosenCategory,
            )
            new_messsage.save()
            return JsonResponse({"pk": new_messsage.pk}, status=201)
        except Category.DoesNotExist:
            return JsonResponse({"error": "Category not found"}, status=404)


@login_required
@csrf_exempt
def delete_data(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            message_pk = body.get("pk")

            if not message_pk:
                return JsonResponse(
                    {"error": "Missing message primary key"}, status=400
                )

            chosenData = ToDoMessage.objects.get(user=request.user, pk=message_pk)
            chosenData.delete()
            return JsonResponse(
                {"success": f"Message with id {message_pk} deleted"}, status=200
            )

        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": "Message not found or not owned by user"}, status=404
            )
        except ValueError:
            # Includes json.JSONDecodeError, which is a subclass of ValueError
            return JsonResponse(
                {"error": "Invalid JSON or missing pk field"}, status=400
            )
        except Exception as e:
            # Catch any other unforeseen errors
            return JsonResponse({"error": str(e)}, status=500)


@login_required
@csrf_exempt
def edit_data(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            message_pk = body.get("pk")
            new_message_data = body.get("newMessageData")

            # You may want to add additional validation here for new_message_data
            if not message_pk or new_message_data is None:
                return JsonResponse(
                    {"error": "Missing message primary key or new data"}, status=400
                )

            chosenData = ToDoMessage.objects.get(user=request.user, pk=message_pk)
            chosenData.message_data = new_message_data
            chosenData.save()
            return JsonResponse({"success": "Message updated successfully"}, status=200)

        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": "Message not found or not owned by user"}, status=404
            )
        except ValueError:
            # Includes json.JSONDecodeError, which is a subclass of ValueError
            return JsonResponse(
                {"error": "Invalid JSON or missing pk field"}, status=400
            )
        except Exception as e:
            # Catch any other unforeseen errors
            return JsonResponse({"error": str(e)}, status=500)


@login_required
@csrf_exempt
def finished_data(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            message_pk = body.get("pk")

            if not message_pk:
                return JsonResponse(
                    {"error": "Missing message primary key"}, status=400
                )

            # Ensure the ToDoMessage exists and is owned by the request user
            chosenData = ToDoMessage.objects.get(pk=message_pk, user=request.user)
            chosenData.is_finished = not chosenData.is_finished
            chosenData.save()
            return JsonResponse(
                {"success": "Message status updated successfully"}, status=200
            )

        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": "Message not found or not owned by user"}, status=404
            )
        except ValueError:
            # Includes json.JSONDecodeError, which is a subclass of ValueError
            return JsonResponse(
                {"error": "Invalid JSON or missing pk field"}, status=400
            )
        except Exception as e:
            # Catch any other unforeseen errors
            return JsonResponse({"error": str(e)}, status=500)


@login_required
@csrf_exempt
def post_category(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            color = body.get("color")
            category_data = body.get("category_data")

            if color is None or category_data is None:
                return JsonResponse(
                    {"error": "Missing color or category data"}, status=400
                )

            new_category = Category(color=color, category_data=category_data)
            new_category.save()
            return JsonResponse(
                {"id": new_category.pk, "color": color, "category_data": category_data},
                status=201,
            )

        except ValueError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["GET"])
def category_json(request):
    category = Category.objects.filter(user=request.user)
    return HttpResponse(
        serializers.serialize("json", category), content_type="application/json"
    )
