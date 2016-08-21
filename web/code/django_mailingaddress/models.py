import re

from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import ugettext_lazy as _
import pycountry

class PycountryManager(models.Manager):
	"""Base manager for any model that shadows a pycountry database."""

	def sync(self):
		""""Syncs the managed model with its pycountry equivalent."""

		model_fields = self.model._meta.get_fields()

		# Clear all existing model instances
		self.all().delete()

		for resource in self.provide_pycountry_database():
			kwargs = {}
			for field_name in model_fields:
				if hasattr(resource, field_name.name):
					kwargs[field_name.name] = getattr(resource, field_name.name)
			self.create(**kwargs)

	def provide_pycountry_database(self):
		"""Provide the pycountry database that the model shadows."""
		raise NotImplementedError

class ISOCountryManager(models.Manager):
	"""Custom manager for the ISOCountry model."""

	def get_by_natural_key(self, alpha3):
		return self.get(alpha3=alpha3)

class ISOCountryPycountryManager(PycountryManager):
	"""Pycountry manager for the ISOCountry model."""

	def provide_pycountry_database(self):
		return pycountry.countries

class ISOCountry(models.Model):
	"""A country covered by the ISO 3166-1 standard."""

	objects   = ISOCountryManager()
	pycountry = ISOCountryPycountryManager()

	alpha2  	  = models.CharField(max_length=2, verbose_name=_("alpha-2 code"), unique=True)
	alpha3  	  = models.CharField(max_length=3, verbose_name=_("alpha-3 code"), unique=True)
	numeric 	  = models.CharField(max_length=3, verbose_name=_("numeric code"))
	name          = models.CharField(max_length=75, verbose_name=_("name"), unique=True)
	slug          = AutoSlugField(max_length=75, verbose_name=_("slug"), populate_from="name", unique=True)
	official_name = models.CharField(max_length=75, verbose_name=_("official name"), null=True, blank=True)

	class Meta:
		ordering = ('name',)
		verbose_name = _("ISO 3166 country")
		verbose_name_plural = _("ISO 3166 countries")

	def __str__(self):
		return self.name

	def natural_key(self):
		return (self.alpha3,)
