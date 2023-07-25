from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = [
        'matric',
        'email',
        'username',
        'cgpa',
        'is_staff',
    ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (

            ),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': (
                'matric',
                'email',
                'first_name',
                'last_name',
                'middle_name',
            )
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
