from django.contrib import admin
from .models import User, Tip

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'created', 'updated', 'has_right_to_delete_tips', 'can_downvote_tips']
    search_fields = ['username']
    readonly_fields = ['created', 'updated']
    list_editable = ['has_right_to_delete_tips', 'can_downvote_tips']


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ['content', 'author', 'created']
    search_fields = ['content', 'author__username']
    readonly_fields = ['created']
