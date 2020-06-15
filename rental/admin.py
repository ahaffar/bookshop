from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from rental.models import User, UserProfile, Book, Author, Publisher, Borrowed
from rental.forms import CustomUserCreationForm, UserChangeForm


# from django.contrib.auth.forms import UserChangeForm


class UserAdmin(auth_admin.UserAdmin):
    add_form = CustomUserCreationForm
    form = UserChangeForm
    fieldsets = (
        (None, {
            'fields': (
                'username', 'password'
            )
        }),
        ('Personal_Info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'is_borrower'
            )
        }),
        ('Permission_Info', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups', 'user_permissions'
            )
        }),
    )
    list_filter = ('is_superuser',
                   'is_active',
                   'is_borrower',
                   'is_staff',
                   'groups',
                   )
    add_fieldsets = (
        (None,
         {
             'classes': 'wide',
             'fields': ('first_name',
                        'last_name',
                        'email',
                        'is_staff',
                        'password1',
                        'password2',
                        'username'
                        ),
         }),
    )
    readonly_fields = ('date_joined', 'last_login',)
    list_display = ('first_name', 'last_name', 'email', 'is_staff')
    filter_horizontal = ('groups', 'user_permissions')
    ordering = ['-date_joined']


class UserProfileAdmin(admin.ModelAdmin):
    add_fieldsets = (
        ('UserProfile', {
            'fields': (
                'bio',
                'user',
            ),
        }),
    )

    fieldsets = (
        ('Information', {
            'fields': (
                'bio',
                'user',
            )
        }),
        ('Important Dates',
         {
             'fields': (
                 'created_on',
                 'last_updated',
             ),
         }),
    )
    readonly_fields = ('created_on', 'last_updated',)
    list_display = ('bio', 'created_on', 'last_updated', 'user')
    ordering = ['-last_updated']
    search_fields = ('user',)
    list_filter = ('last_updated',
                   )


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Borrowed)

# Register your models here.
