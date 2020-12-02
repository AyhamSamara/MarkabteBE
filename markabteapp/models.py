from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Order(models.Model):
    order = models.TextField()
    entered_by = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=0)
