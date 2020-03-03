from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


admin.site.site_header = "GTUC ELECTIONS"


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = get_user_model()
    list_display = ['email', 'username', 'is_student']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_student')}
        ),
    )




admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Election)

# Group
admin.site.unregister(Group)