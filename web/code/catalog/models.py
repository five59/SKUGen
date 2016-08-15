from django.db import models
from django.utils.translation import ugettext as _
from candybar.CandyBarPdf417 import CandyBarPdf417
import io, os
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from django.core.files.base import ContentFile

# Product Brand
class Brand(models.Model):
    """( Brand description)"""
    id = models.AutoField(_('Code'), primary_key=True)
    name = models.CharField(_('Name'), max_length=64, default="", blank=True)
    code = models.CharField(_('Code'), max_length=3, default="", blank=False,
                            help_text="Three-Character")
    def save(self, *args, **kwargs):
        # Always make the codeeviation uppercase
        self.code = self.code.upper()
        super(Brand, self).save(*args, **kwargs)
    def __str__(self):
        return "{} / {}".format(self.code, self.name)
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

# Product Vendor
class Vendor(models.Model):
    """( Vendor description)"""
    id = models.AutoField(_('Code'), primary_key=True)
    name = models.CharField(_('Name'), max_length=64, default="", blank=True)
    code = models.CharField(_('Code'), max_length=2, default="", blank=False,
                            help_text="Two-Characters")
    def save(self, *args, **kwargs):
        # Always make the codeeviation uppercase
        self.code = self.code.upper()
        super(Vendor, self).save(*args, **kwargs)
    def __str__(self):
        return "{} / {}".format(self.code, self.name)
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")

class Category(MPTTModel):
    """( Category description)"""
    id = models.AutoField(_('Code'), primary_key=True)
    name = models.CharField(_('Name'), max_length=64, default="", blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    def __str__(self):
        return "{}".format(self.name)
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

class Product(models.Model):
    """( Product description)"""
    id = models.AutoField(_('Code'), primary_key=True)
    name = models.CharField(_('Name'), max_length=64, default="", blank=True)
    gtin_id = models.CharField(_('GTIN'), max_length=15, default="", blank=True,
                               help_text="Global Idenfiier.")
    mpn_id = models.CharField(_("MPN"), max_length=64, default="", blank=True,
                              help_text="Manufacturer's Part Number")
    brand = models.ForeignKey(Brand, null=True)
    vendor = models.ForeignKey(Vendor, null=True)
    category = TreeForeignKey(Category, null=True)
    barcode_pdf417 = models.ImageField(upload_to="product_pdf417/", null=True, blank=True)

    def get_sku(self):
        rv = "{}{}-{:03d}-{:04d}".format(
            self.brand.code,
            self.vendor.code,
            self.category.id,
            self.id
        )
        return rv
    get_sku.short_description = _('Base SKU')

    def get_numvariants(self):
        rv = ProductVariant.objects.filter(product = self.id).count()
        return rv
    get_numvariants.short_description = _('Variant SKUs')

    def get_variants(self):
        rv = ProductVariant.objects.filter(product = self.id)
        return rv
    get_variants.short_description = _('Variants')

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):

        # Generate the barcode using CandyBar.
        # Note: django-cleanup handles deleting the file if variant is deleted.
        if not self.barcode_pdf417:
            pdf417 = CandyBarPdf417()
            barcode_bytestring = pdf417.encode(self.get_sku())
            filename = "{}.png".format(
                os.path.join(
                    settings.MEDIA_ROOT, 'product_pdf417', self.get_sku() ))
            self.barcode_pdf417.save(filename, ContentFile(barcode_bytestring))

        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


    # def gtin_type(self):
    #     # NOT IMPLEMENTED
    #     # UPC / GTIN-12 / UPC-A	-- 12 length
    #     # EAT / GTIN-13 -- 8, 13 or 14 length
    #     # JAN / GTIN-13 -- 13 length
    #     return 0

class ProductVariant(models.Model):
    """( ProductVariant description)"""
    id = models.AutoField(_('Code'), primary_key=True)
    product = models.ForeignKey(Product)
    name = models.CharField(_('Name'), max_length=64, default="", blank=True)
    code = models.CharField(_('Code'), max_length=3, default="", blank=False,
                            help_text="Three-Character")
    gtin_id = models.CharField(_('GTIN'), max_length=15, default="", blank=True,
                               help_text="Global Idenfiier.")
    mpn_id = models.CharField(_("MPN"), max_length=64, default="", blank=True,
                              help_text="Manufacturer's Part Number")
    barcode_pdf417 = models.ImageField(upload_to="product_pdf417/", null=True, blank=True)

    def get_sku(self):
        rv = "{}-{}".format(self.product.get_sku(), self.code)
        return rv
    get_sku.short_description = _("Variant SKU")

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):

        # Generate the barcode using CandyBar.
        # Note: django-cleanup handles deleting the file if variant is deleted.
        if not self.barcode_pdf417:
            pdf417 = CandyBarPdf417()
            barcode_bytestring = pdf417.encode(self.get_sku())
            filename = "{}.png".format(
                os.path.join(
                    settings.MEDIA_ROOT, 'product_pdf417', self.get_sku() ))
            self.barcode_pdf417.save(filename, ContentFile(barcode_bytestring))

        super(ProductVariant, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Variant"
        verbose_name_plural = "Variants"
