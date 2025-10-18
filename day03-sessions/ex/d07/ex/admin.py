from django.contrib import admin
from .models import User, Tip

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'created', 'updated', 'get_reputation']
    search_fields = ['username']
    readonly_fields = ['created', 'updated']
    filter_horizontal = ['user_permissions']
    
    def get_reputation(self, obj):
        return obj.get_reputation()
    get_reputation.short_description = 'Reputation'


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ['content', 'author', 'created']
    search_fields = ['content', 'author__username']
    readonly_fields = ['created']
