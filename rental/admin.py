from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from rental.models import User, UserProfile, Book, Author, Publisher, Borrowed
from rental.forms import CustomUserCreationForm, UserChangeForm
# from django.contrib.auth.forms import UserChangeForm


class UserAdmin(auth_admin.UserAdmin):
    add_form = CustomUserCreationForm
    form = UserChangeForm
    add_fieldsets = (
        None, {
            'classes': 'wide',
            'fields': ('first-name',
                       'last_name',
                       'email',
                       'is_staff',
                       'password1',
                       'password2'),
        },
    )
    readonly_fields = ('date_joined', 'last_login', 'email')
    list_display = ('first_name', 'last_name', 'email', 'is_staff')
    filter_horizontal = ('groups', 'user_permissions')
    ordering = ['-date_joined']


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Borrowed)

# Register your models here.
