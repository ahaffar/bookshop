from rest_framework import viewsets, renderers, status
from rest_framework import generics
from rest_framework.response import Response
from rental import serializers, permissions, models
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import permissions as rest_permissions
from django.contrib.auth import models as django_models


class UserViewSets(viewsets.ModelViewSet):
    """
    API View for User Serializer
    """
    serializer_class = serializers.UserSerializer
    # permission_classes = [permissions.UserPermission,
    #                       ]
    authentication_classes = [TokenAuthentication, ]
    queryset = models.User.objects.all()
    renderer_classes = [renderers.AdminRenderer, ]
    permission_classes = [rest_permissions.IsAuthenticated, permissions.UserViewPermissions]


class AuthUser(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class GroupViews(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = django_models.Group.objects.all()
    renderer_classes = [renderers.AdminRenderer, renderers.JSONRenderer, renderers.BrowsableAPIRenderer]
    lookup_field = 'name'


class UserProfileViewSets(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication, ]
    permission_classes = [rest_permissions.IsAuthenticated, permissions.UserProfileOwnerUpdate, ]
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    renderer_classes = [renderers.AdminRenderer, renderers.JSONRenderer, renderers.BrowsableAPIRenderer, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublisherViewSets(viewsets.ModelViewSet):
    serializer_class = serializers.PublisherSerializer
    queryset = models.Publisher.objects.all()


class BorrowedViewSet(viewsets.ModelViewSet):
    queryset = models.Borrowed.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = [rest_permissions.IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]



