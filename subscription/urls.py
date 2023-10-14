from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterViewSet,
    LoginViewSet,
    PackageViewSet,
    SubscriptionViewSet,
    UserSubscriptionsViewSet
)
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('register', RegisterViewSet)
router.register('login', LoginViewSet, basename='login')
router.register('package', PackageViewSet)
router.register('subscription', SubscriptionViewSet)
router.register('user-subscriptions', UserSubscriptionsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("login/", obtain_auth_token, name="login")
]
