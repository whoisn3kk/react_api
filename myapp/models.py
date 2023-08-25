import uuid
from django.db import models


class Api(models.Model):
	id = models.AutoField(primary_key=True)
	uuid = models.CharField(max_length=320, default=uuid.uuid4)
	json = models.TextField(null=True)