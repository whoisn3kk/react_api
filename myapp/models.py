import uuid
from django.db import models


class Api(models.Model):
	id = models.AutoField(primary_key=True)
	uuid = models.CharField(max_length=320, default=uuid.uuid4)
	json = models.TextField(null=True)

class Products(models.Model):
	uuid = models.CharField(max_length=320, default=uuid.uuid4)
	title = models.TextField()
	price = models.IntegerField()
	imageUrl = models.CharField(max_length=320)

class Cart(models.Model):
	product_link = models.ForeignKey(Products, on_delete=models.CASCADE)

class Likes(models.Model):
	product_link = models.ForeignKey(Products, on_delete=models.CASCADE)