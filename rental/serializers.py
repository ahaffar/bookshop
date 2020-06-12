from rest_framework import serializers
from django_countries import serializers as countries_serializers
from rental import models
from django.contrib.auth.models import Group, Permission
from rental.apps import RentalConfig


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializers User Model
    """
    # url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'url', 'username']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'url': {
                'lookup_field': 'username'
            },
            'email': {
                'read_only': True
            },
        }

    def create(self, validated_data):
        user = models.User(email=validated_data['email'],
                           first_name=validated_data['first_name'],
                           last_name=validated_data['last_name'])
        password = user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

            return super().update(instance, validated_data)


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = models.UserProfile
        fields = ['id', 'user', 'bio', 'created_on', 'url']
        extra_kwargs = {
            'created_on': {
                'read_only': True
            },
            'user': {
                'read_only': True
            }
        }


class PublisherSerializer(countries_serializers.CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Publisher
        fields = ['id', 'name', 'country', 'website']


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializers Author Model
    """

    class Meta:
        model = models.Author
        fields = ['id', 'first_name', 'last_name', 'email']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class BorrowedSerializer(serializers.ModelSerializer):
    """
    serializes Borrowed Model
    """

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
