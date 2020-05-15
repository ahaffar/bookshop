from django.contrib import admin
from rental.models import User, UserProfile, Book, Author, Publisher, Borrowed

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Borrowed)

# Register your models here.
