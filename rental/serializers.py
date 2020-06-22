from rest_framework import serializers
from django_countries import serializers as countries_serializers
from rental import models
from django.contrib.auth.models import Group, Permission
from rental.apps import RentalConfig
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializers User Model
    """
    # url = serializers.CharField(source='get_absolute_url', read_only=True)
    url = serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='username', read_only=True)
    author = serializers.SlugRelatedField(source='authors', slug_field='is_author',
                                          read_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'url', 'username', 'author']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
        }

    def create(self, validated_data):
        user = models.User(email=validated_data['email'],
                           first_name=validated_data['first_name'],
                           last_name=validated_data['last_name'],
                           username=validated_data['username'])
        password = user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

            return super().update(instance, validated_data)


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='user.username', read_only=True)
    url = serializers.HyperlinkedRelatedField(read_only=True, view_name='userprofile-detail', )

    class Meta:
        model = models.UserProfile
        fields = ['user', 'bio', 'created_on', 'url']
        extra_kwargs = {
            'last_updated': {
                'read_only': True
            },
            'user': {
                'read_only': True
            },
        }


class PublisherSerializer(countries_serializers.CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Publisher
        fields = ['id', 'name', 'country', 'website']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializers Author Model
    """

    # first_name = serializers.SlugRelatedField(source='author', slug_field='first_name',
    #                                           read_only=True)
    # last_name = serializers.SlugRelatedField(source='author', slug_field='last_name',
    #                                          read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.filter(groups__name='Authors'),
                                                write_only=True)
    name = serializers.SerializerMethodField()
    username = serializers.PrimaryKeyRelatedField(source='author.username', read_only=True)
    url = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

    class Meta:
        model = models.Author
        fields = ['author', 'username', 'url', 'name']

    def get_name(self, author):
        return '%s %s' % (author.author.first_name, author.author.last_name)


class BookSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(queryset=models.Genre.objects.all(), slug_field='name',
                                         many=True)
    publisher = serializers.SlugRelatedField(slug_field='name', queryset=models.Publisher.objects.all())
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Author.objects.all(),
                                                 source='author', write_only=True)
    author = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Book
        fields = ['title', 'genre', 'author', 'publisher', 'published_date', 'isbn', 'language', 'authors']


class BorrowedSerializer(serializers.ModelSerializer):
    """
    serializes Borrowed Model
    """
    user = serializers.PrimaryKeyRelatedField(help_text='username of the borrower',
                                              queryset=User.objects.filter(is_borrower=1))

    class Meta:
        model = models.Borrowed
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.SlugRelatedField(many=True, queryset=models.User.objects.filter(is_superuser=0),
                                         source='user_set', slug_field='email')
    permissions = serializers.SlugRelatedField(many=True, queryset=Permission.objects.filter(
        content_type__app_label=RentalConfig.name), slug_field='name')

    class Meta:
        model = Group
        fields = ['users',
                  'name', 'permissions', 'url']
        extra_kwargs = {
            'url': {
                'lookup_field': 'name'
            }
        }
