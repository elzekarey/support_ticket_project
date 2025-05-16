from django.contrib.auth.models import AbstractUser
from django.db import models

#User
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)

#Customer
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

#Ticket
class Ticket(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'is_agent': True})
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=[('unassigned', 'Unassigned'), ('assigned', 'Assigned'), ('sold', 'Sold')], default='unassigned')