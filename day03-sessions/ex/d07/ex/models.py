from django.db import models
from django.db.models import Count
from django.contrib.auth.hashers import make_password, check_password

UPVOTE_REPUTATION_POINTS = 5
DOWNVOTE_REPUTATION_POINTS = -2
DOWNVOTE_REPUTATION_THRESHOLD = 15
DELETE_REPUTATION_THRESHOLD = 30


class User(models.Model):
    username = models.CharField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    has_right_to_delete_tips = models.BooleanField(default=False)
    can_downvote_tips = models.BooleanField(default=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_reputation(self):
        tips_stats = self.tip_set.aggregate(
            total_upvotes=Count("upvoted_by"), total_downvotes=Count("downvoted_by")
        )
        return (tips_stats["total_upvotes"] or 0) * UPVOTE_REPUTATION_POINTS + (
            tips_stats["total_downvotes"] or 0
        ) * DOWNVOTE_REPUTATION_POINTS

    def can_downvote(self):
        return (
            self.get_reputation() >= DOWNVOTE_REPUTATION_THRESHOLD or self.can_downvote
        )

    def can_delete_tips(self):
        return (
            self.get_reputation() >= DELETE_REPUTATION_THRESHOLD
            or self.has_right_to_delete_tips
        )

    def __str__(self):
        return self.username


class Tip(models.Model):
    content = models.TextField(null=False)
    author = models.ForeignKey(
        User, to_field="username", on_delete=models.CASCADE, null=False
    )
    created = models.DateField(auto_now_add=True, null=True)
    upvoted_by = models.ManyToManyField(User, related_name="upvoted_tips", blank=True)
    downvoted_by = models.ManyToManyField(
        User, related_name="downvoted_tips", blank=True
    )

    def __str__(self):
        return f"Tip: {self.content} Author: {self.author}. Created: {self.created}"
