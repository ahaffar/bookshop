from django.db import models
from django.db.models import Case, When, IntegerField, Value
from bookshop import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.contrib.auth import validators
from django_countries import fields
from datetime import datetime, timedelta


class UserManager(BaseUserManager):
    """"
    Model Manager for the User Model
    """
    def create_user(self, email, first_name, last_name, username, password=None):
        if not email:
            raise ValueError('a valid email address is required')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password):
        user = self.create_user(email, first_name, last_name, username, password)
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
    username = models.CharField(max_length=15, unique=True, null=True, blank=False,
                                validators=(validators.UnicodeUsernameValidator, ))
    is_borrower = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def is_admin(self):
        return self.groups.filter(name='librarians').exists()


class Genre(models.Model):
    name = models.CharField(max_length=30, help_text='The name of genre such as Drama, Art...')

    def __str__(self):
        return self.name


class Author(models.Model):
    """
    A Model to store the Authors info
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    is_author = models.BooleanField(default=True, editable=True, )

    def __str__(self):
        return self.author.username


class Publisher(models.Model):
    name = models.CharField(max_length=100, blank=False, help_text='Publisher Name')
    country = fields.CountryField(blank_label='(select country)')
    website = models.URLField()

    def __str__(self):
        return self.name


class Book(models.Model):

    class BookLanguage(models.TextChoices):
        EN = 'EN', 'ENGLISH'
        AR = 'AR', 'ARABIC'
        FR = 'FR', 'FRENCH'
        DE = 'DE', 'GERMAN'
        ES = 'ES', 'SPANISH'
        PT = 'PT', 'PORTUGUESE'

    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    author = models.ManyToManyField(Author, related_name='books')
    title = models.CharField(max_length=80, blank=False)
    published_date = models.DateField(null=True, blank=False)
    genre = models.ManyToManyField(Genre, related_name='books')
    isbn = models.CharField('ISBN', max_length=13, help_text='The ISBN of the Book - 13 Chars', default='XXXXXXXXXX')
    language = models.CharField(max_length=2, choices=BookLanguage.choices, default=BookLanguage.EN)

    def __str__(self):
        return self.title


class Borrowed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='username of the borrower',
                             on_delete=models.DO_NOTHING, related_name='borrowings')
    borrowed_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(Book, on_delete=models.DO_NOTHING, verbose_name='book')
    returned_date = models.DateField(blank=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, )
    is_returned = models.BooleanField(default=False,)
    # False in order to hide it from admin
    due_back = models.DateTimeField(default=datetime.now()+timedelta(days=1))

    class Meta:
        ordering = ['-borrowed_date']

    def __str__(self):
        return '%s - Borrowed By (%s)' % (self.title, self.user)

    @property
    def is_overdue(self):
        if self.due_back and datetime.now() > self.due_back:
            return True


# class BookLimit(models.QuerySet):
#     def book_limit(self):
#         self.annotate(borrow_limit=Case(When(UserProfile.UserType.FREE, then=Value(1)),
#                                         When(UserProfile.UserType.BASIC, then=Value(2)),
#                                         When(UserProfile.UserType.PREMIUM, then=Value(5)),
#                                         default=Value(1), output_field=IntegerField))
#

# class ProfilePlanManager(models.Manager):
#     def get_queryset(self):
#         return BookLimit(self.model, using=self._db)


class UserProfileManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            book_limit=Case(
                When(user_type=UserProfile.UserType.FREE, then=Value(1)),
                When(user_type=UserProfile.UserType.BASIC, then=Value(2)),
                When(user_type=UserProfile.UserType.PREMIUM, then=Value(5)),
                default=Value(1),
                output_field=IntegerField()
            )
        )


class UserProfile(models.Model):
    class UserType(models.TextChoices):
        FREE = 'FR', 'FREE'
        BASIC = 'BS', 'BASIC'
        PREMIUM = 'PR', 'PREMIUM'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user_type = models.CharField(max_length=2, choices=UserType.choices, default=UserType.FREE)

    objects = UserProfileManager()

    def __str__(self):
        return self.user.username

