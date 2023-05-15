from django.contrib import admin
from .models import User, VerifideUser

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_verified_email')
    fields = (('first_name', 'last_name', 'username', 'email'), 
              ('is_superuser', 'is_staff', 'is_verified_email', 'is_active'), 
              ('date_joined', 'last_login'), 'image',
              ('groups', 'user_permissions'), 'password')
    readonly_fields = ('password', 'email', 'last_login', 'date_joined')


@admin.register(VerifideUser)
class VerifiedUserAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'created', 'expiration')
    fields = (('code', 'user'), ('created', 'expiration'))
    readonly_fields = ('created', 'user', 'code')
