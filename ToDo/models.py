from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_data = models.TextField()
    color = models.TextField()


class ToDoMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_data = models.TextField()
    date_data = models.DateTimeField(null=True)
    is_finished = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
