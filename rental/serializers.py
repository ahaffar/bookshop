from rest_framework import serializers
from rental.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializers User Model
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
            user = User(email=validated_data['email'],
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
