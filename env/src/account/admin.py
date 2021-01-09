from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'display_name',  'date_joined', 'last_login', 'is_staff', 'is_admin')
    search_fields = ('email',  'display_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('date_joined', 'display_name')
    list_filter = ('is_editor', 'is_super_editor',)
    filter_horizontal = ()
    fieldsets = ()
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('email', 'display_name',  'password1', 'password2', 'profile_picture'),
    }),
    )

admin.site.register(Account, AccountAdmin)