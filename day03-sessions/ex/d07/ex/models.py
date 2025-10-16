from django.db import models
from django.contrib.auth.hashers import make_password, check_password

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


class Tip(models.Model):
    content = models.TextField(null=False)
    author = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, null=False)
    created = models.DateField(auto_now_add=True, null=True)
    upvoted_by = models.ManyToManyField(User, related_name='upvoted_tips', blank=True)
    downvoted_by = models.ManyToManyField(User, related_name='downvoted_tips', blank=True)

    def __str__(self):
        return f"Tip: {self.content} Author: {self.author}. Created: {self.created}"
