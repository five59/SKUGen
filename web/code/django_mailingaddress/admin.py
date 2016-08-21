from django.contrib import admin
from .models import *


class ISOCountryAdmin(admin.ModelAdmin):
	list_display  = ('alpha2', 'alpha3', 'numeric', 'name', 'official_name')
	ordering      = ('name',)
	search_fields = ('name', 'official_name')

admin.site.register(ISOCountry, ISOCountryAdmin)
