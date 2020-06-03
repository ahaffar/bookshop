from rental import views
from rest_framework import routers
from django.urls import path, include

router = routers.SimpleRouter()
router.register('users', views.UserViewSets,)
router.register('bio', views.UserProfileViewSets, )
router.register('publishers', views.PublisherViewSets, )
router.register('borrow', views.BorrowedViewSet, )

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.AuthUser.as_view(), name='auth')
]
