from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass



# Create your models here.

class Todo(models.Model):
    name =models.CharField( max_length=50)
    subject =models.TextField()
    email =models.EmailField(max_length=254)



