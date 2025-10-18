from django.db import models
from django.db.models import Count
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Permission

UPVOTE_REPUTATION_POINTS = 5
DOWNVOTE_REPUTATION_POINTS = -2
DOWNVOTE_REPUTATION_THRESHOLD = 15
DELETE_REPUTATION_THRESHOLD = 30


class User(models.Model):
    username = models.CharField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_user_set',
        verbose_name='user permissions',
    )

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

    def has_perm(self, perm):
        if '.' in perm:
            app_label, codename = perm.split('.')
            return self.user_permissions.filter(
                content_type__app_label=app_label,
                codename=codename
            ).exists()
        return False

    def can_downvote(self):
        return (
            self.get_reputation() >= DOWNVOTE_REPUTATION_THRESHOLD 
            or self.has_perm('ex.can_downvote_tips')
        )

    def can_delete_tips(self):
        return (
            self.get_reputation() >= DELETE_REPUTATION_THRESHOLD
            or self.has_perm('ex.delete_tip')
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

    class Meta:
        permissions = [
            ("can_downvote_tips", "Can downvote tips"),
        ]

    def __str__(self):
        return f"Tip: {self.content} Author: {self.author}. Created: {self.created}"
