from rest_framework import viewsets, renderers
from rental import serializers, permissions, models
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import permissions as rest_permissions


class UserViewSets(viewsets.ModelViewSet):
    """
    API View for User Serializer
    """
    queryset = models.User.objects.none()
    serializer_class = serializers.UserSerializer
    permission_classes = [rest_permissions.IsAuthenticated, permissions.UserUpdatePermission,
                          permissions.UserViewPermissions, rest_permissions.DjangoModelPermissions]
    authentication_classes = [TokenAuthentication, ]
    renderer_classes = [renderers.AdminRenderer, ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.User.objects.all()
        return models.User.objects.filter(id=self.request.user.id)


class AuthUser(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


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





