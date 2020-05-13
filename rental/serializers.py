from rest_framework import serializers
from rental import models


class UserSerializer(serializers.ModelSerializer):
    """
    Serializers User Model
    """
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'url']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
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
