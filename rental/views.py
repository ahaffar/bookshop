from rest_framework import viewsets, renderers, status
from rest_framework.decorators import action
from rest_framework import serializers as rest_serializers
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
    renderer_classes = [renderers.AdminRenderer, renderers.BrowsableAPIRenderer, renderers.JSONRenderer]
    permission_classes = [rest_permissions.IsAuthenticated, permissions.UserViewPermissions]
    lookup_field = 'username'


class AuthUser(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class GroupViews(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = django_models.Group.objects.all()
    renderer_classes = [renderers.AdminRenderer, renderers.JSONRenderer, renderers.BrowsableAPIRenderer]
    lookup_field = 'name'
    permission_classes = [rest_permissions.IsAdminUser]


class UserProfileViewSets(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [rest_permissions.IsAuthenticated, permissions.UserProfileOwnerUpdate, ]
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    renderer_classes = [renderers.AdminRenderer, renderers.JSONRenderer, renderers.BrowsableAPIRenderer, ]
    lookup_field = 'user'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        queryset = self.filter_queryset(models.UserProfile.objects.get(user__username=self.kwargs.get('user')))
        return queryset

    @action(detail=True, url_name='borrow', url_path='borrow', description='List Books Borrowed by User',
            permission_classes=[permissions.IsOwner, ])
    def borrowed_books(self, request, **kwargs):
        borrowed = self.filter_queryset(models.Borrowed.objects.filter(user__username=self.kwargs.get('user'),))
        serializer = serializers.BorrowedSerializer(borrowed, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublisherViewSets(viewsets.ModelViewSet):
    serializer_class = serializers.PublisherSerializer
    queryset = models.Publisher.objects.all()

    @action(methods=["GET", ], detail=True, url_path='books', url_name='name')
    def publisher_list_books(self, request, **kwargs):
        books = self.filter_queryset(models.Book.objects.filter(publisher=self.kwargs.get('pk')))
        serialized_books = serializers.BookDetailedSerializer(books, many=True)
        return Response(serialized_books.data, status=status.HTTP_200_OK)


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AuthorSerializer
    queryset = models.Author.objects.all()
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer, renderers.AdminRenderer]
    # the below is not used but i keep it for reference
    # lookup_field = 'author__username'
    # the below should match the kwargs in the customized HyperLinkedIdentityField
    lookup_field = 'obj_username'
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.ReadOnlyPermission, ]

    def get_object(self):
        queryset = self.filter_queryset(models.Author.objects.get(author__username=self.kwargs.get('obj_username')))
        return queryset

    @action(detail=True, url_name='books', url_path='books', )
    def author_book_list(self, request, **kwargs):
        """
        retrieve the books list for the related author
        """
        books = models.Book.objects.filter(author__author__username=self.kwargs.get('obj_username'))
        serialized_books = serializers.BookDetailedSerializer(books, many=True)
        return Response(serialized_books.data, status=status.HTTP_200_OK)


class BorrowedViewSet(viewsets.ModelViewSet):
    queryset = models.Borrowed.objects.all()
    serializer_class = serializers.BorrowedSerializer
    permission_classes = [permissions.IsAdmin, ]
    authentication_classes = [TokenAuthentication, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = models.UserProfile.objects.get(user=serializer.validated_data['user'])
        borrowed_book_count = models.Borrowed.objects.filter(user=serializer.validated_data['user'],
                                                             is_returned=False).count()
        error_msg = [
            "The user package ('%s') not allowing to rent more than %s book(s)" % (profile.user_type, profile.book_limit),
            "Current rented books are : %s" % (models.Borrowed.objects.get(user=serializer.validated_data['user'],
                                                                         is_returned=False))
        ]
        if profile.book_limit == borrowed_book_count:
            raise rest_serializers.ValidationError(detail=error_msg,
                                                   code=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookListSerializer
    renderer_classes = [renderers.AdminRenderer, renderers.JSONRenderer, renderers.BrowsableAPIRenderer]
    queryset = models.Book.objects.all()
    lookup_field = 'slug'
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.BookSerializer]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.BookListSerializer
        return serializers.BookDetailedSerializer


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GenreSerializer
    queryset = models.Genre.objects.all()
    permission_classes = [permissions.IsAdmin, ]
    authentication_classes = [TokenAuthentication]

    @action(methods=["GET"], detail=True, name='books', url_path='books')
    def list_books(self, request, **kwargs):
        books = self.filter_queryset(models.Book.objects.filter(genre=self.kwargs.get('pk')))
        serialized_books = serializers.BookDetailedSerializer(books, many=True)
        return Response(serialized_books.data, status=status.HTTP_200_OK)
