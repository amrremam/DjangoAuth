from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.base import RedirectView
# from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),

    path('admin/', admin.site.urls),
    path('api/', include('subscription.urls')),
    # path('tokenrequest/', obtain_auth_token),
]
