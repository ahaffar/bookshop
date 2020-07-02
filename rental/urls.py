from rental import views
from rest_framework import routers
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.authentication import TokenAuthentication

router = routers.DefaultRouter()
router.register(
    "users", views.UserViewSets,
)
router.register(
    "bio", views.UserProfileViewSets,
)
router.register(
    "publishers", views.PublisherViewSets,
)
router.register(
    "borrow", views.BorrowedViewSet,
)
router.register(
    "groups", views.GroupViews,
)
router.register("authors", views.AuthorViewSet)
router.register("books", views.BookViewSet)
router.register("genre", views.GenreViewSet)

DYNAMIC_VIEW = [
    path(
        "schema/",
        get_schema_view(
            title="Bookshop API Docs",
            description="Dynamic Schema for OpenAPI documenting Bookshop APIs",
            authentication_classes=[TokenAuthentication],
        ),
        name="openapi",
    )
]

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", views.AuthUser.as_view(), name="auth"),
    # path('authors/<str:username>/books', views.AuthorViewSet.as_view({'get': 'author_book_list'}), name='books'),
]

urlpatterns += DYNAMIC_VIEW
