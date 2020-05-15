from django.db import models
from bookshop import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django_countries import fields


class UserManager(BaseUserManager):
    """"
    Model Manager for the User Model
    """
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('a valid email address is required')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """"
    Customizes the default user account
    """
    email = models.EmailField(unique=True, help_text='username is the email address')
    first_name = models.CharField(max_length=40, blank=False)
    last_name = models.CharField(max_length=40, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Author(models.Model):
    """
    A Model to store the Authors info
    """
    first_name = models.CharField(max_length=40, blank=False, help_text='First name')
    last_name = models.CharField(max_length=40, blank=False, help_text='Last name')
    email = models.EmailField()

    def __str__(self):
        return '%s %sa' %(self.first_name, self.last_name)


class Publisher(models.Model):
    name = models.CharField(max_length=100, blank=False, help_text='Publisher Name')
    country = fields.CountryField(blank_label='(select country)')
    website = models.URLField()

    def __str__(self):
        return self.name


class Book(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=80, blank=False)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title