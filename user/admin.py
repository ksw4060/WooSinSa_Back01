from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.forms import UserCreationForm, UserChangeForm


# Register your models here.
# Now register the new UserAdmin...


# 작성자 : 김성우
# 내용 : 어드민 페이지에 유저등록, 리스트와 필드셋 설정, UserCreationForm과 UserChangeForm는 forms.py에 작성
# 최초 작성일 :23년6월7일
# 업데이트 일자 :23년6월7일
class MyUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id", "account", "email", "username",
                     "age", "gender","is_active", "is_admin", "joined_at", "phone_number",]
    list_filter = ["is_active", "is_admin"]
    fieldsets = [
        ("User Information", {"fields": ["account", "username", "age", "gender", "password", "phone_number", ]}),
        ("Permissions", {"fields": ["is_active", "is_admin",]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["account", "email", "password1", "password2", "phone_number"],
            },
        ),
    ]
    search_fields = ["account"]
    ordering = ["account"]
    filter_horizontal = []

admin.site.register(User, MyUserAdmin)
