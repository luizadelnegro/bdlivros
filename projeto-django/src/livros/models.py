from django.db import models

class Book(models.Model):
	titulo=models.CharField(unique=True,max_length=30, null=False)
	autor=models.CharField(max_length=30, null=False)
	editora=models.CharField(max_length=30, null=False)
