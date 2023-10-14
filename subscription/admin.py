from django.contrib import admin
from .models import Package, Subscription

admin.site.site_header = 'Bit68'
admin.site.site_title = 'Bit68'


admin.site.register(Package)
admin.site.register(Subscription)
