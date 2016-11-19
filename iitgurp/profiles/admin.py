from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import UserProfile, Faculty, Student

admin.site.site_header = 'IITG FSC Portal'


class UserProfileChangeForm(UserChangeForm):
    """
    Subclass of UserChangeForm used for form field in UserProfileAdmin
    """
    class Meta(UserChangeForm.Meta):
        model = UserProfile


class UserProfileCreationForm(UserCreationForm):
    """
    Subclass of UserCreationForm used for add_form field in UserProfileAdmin
    """
    class Meta(UserCreationForm.Meta):
        model = UserProfile


class UserProfileAdmin(UserAdmin):
    """
    Class that represents UserProfile model in the admin interface.
    """
    form = UserProfileChangeForm
    add_form = UserProfileCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    list_display = ('username', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active')
    search_fields = ('username',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Faculty)
admin.site.register(Student)
