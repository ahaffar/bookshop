from rental import views
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register('user', views.UserViewSets,)
router.register('bio', views.UserProfileViewSets, )

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.AuthUser.as_view(), name='auth')
]
