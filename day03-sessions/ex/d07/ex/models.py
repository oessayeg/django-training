from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
