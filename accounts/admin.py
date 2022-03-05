from django.contrib import admin

# Register your models here.
from accounts.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'id']