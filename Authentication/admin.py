from django.contrib import admin
from Authentication.models import UserModel


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'zipcode', 'is_verified', 'is_staff']


admin.site.register(UserModel, UserAdmin)
