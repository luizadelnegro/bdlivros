from django.db import models
from django.conf import settings
from livros.models import Book


class User(models.Model):
	nome=models.CharField(max_length=30, null=False)
	email=models.EmailField(max_length=30, null=False, unique=True)
	login=models.CharField(max_length=30, null=False, unique=True)
	password=models.CharField(max_length=1000, null=False)
	mybooks=models.ManyToManyField(Book)
	

