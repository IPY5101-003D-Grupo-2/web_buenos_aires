from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey
from django.db.models.fields import BooleanField, CharField, PositiveIntegerField, TextField

# Create your models here.
User = get_user_model()


class CarritoDeCompra(models.Model):
    usuario = ForeignKey(User, related_name="carritos", on_delete=CASCADE)
    sku = TextField()
    cantidad = PositiveIntegerField(default=1)
