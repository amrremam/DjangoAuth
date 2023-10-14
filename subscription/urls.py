from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, LoginViewSet

router = DefaultRouter()
router.register('register', RegisterViewSet)
router.register('login', LoginViewSet, basename='login')


urlpatterns = [
    path('', include(router.urls)),
]