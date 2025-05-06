from django.contrib import admin

from marketplace.models import Energy, Energy_Type
# Register your models here.
admin.site.register(Energy_Type)
admin.site.register(Energy)
