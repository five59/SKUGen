import io, os

from django.db import models
from django_mailingaddress.models import *
from mptt.models import MPTTModel, TreeForeignKey

from django.utils.translation import ugettext as _

from candybar.CandyBarPdf417 import CandyBarPdf417
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .forms import *

# Product Brand
class Brand(models.Model):
    """( Brand description)"""
    id = models.AutoField(_('Code'), primary_key=True)
    name = models.CharField(_('Name'), max_length=64, default="", blank=True)
    code = models.CharField(_('Code'), max_length=3, default="", blank=False,
                            help_text="Three-Character")
    website = models.URLField(_("Web Site"), blank=True, default="")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=20)

    def get_numproduct(self):
        rv = Product.objects.filter(brand=self.id).count()
        return rv
    get_numproduct.short_description = _('Product Count')

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
    """( Vendor description )"""
    id = models.AutoField(_('Code'), primary_key=True)
    name = models.CharField(_('Name'), max_length=64, default="", blank=True)
    code = models.CharField(_('Code'), max_length=2, default="", blank=False,
                            help_text="Two-Characters")
    reg_no = models.CharField(_("Local Registration Number"), max_length=64,
                              default="", blank=True)

    address_line1 = models.CharField("Address line 1", max_length = 45,
        blank = True)
    address_line2 = models.CharField("Address line 2", max_length = 45,
        blank = True)
    postal_code = models.CharField("Postal Code", max_length = 10, blank=True)
    city = models.CharField(max_length = 50, blank=True)
    state_province = models.CharField("State/Province", max_length = 40,
        blank = True)
    country = models.ForeignKey(ISOCountry, null=True, blank=True)

    website = models.URLField(_("Web Site"), blank=True, default="")

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    tel_voice = models.CharField(validators=[phone_regex], blank=True, max_length=20)
    tel_fax = models.CharField(validators=[phone_regex], blank=True, max_length=20)

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
    def get_numproduct(self):
        rv = Product.objects.filter(category=self.id).count()
        return rv
    get_numproduct.short_description = _('Product Count')

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
                               help_text="Global Trade Item Number",
                               validators=[validate_gtin]
                               )
    mpn_id = models.CharField(_("MPN"), max_length=64, default="", blank=True,
                              help_text="Manufacturer's Part Number")

    asin_id = models.CharField(_("ASIN"), max_length=10, default="", blank=True,
                               help_text=_("Amazon Standard ID Number"))

    brand = models.ForeignKey(Brand, null=True)
    vendor = models.ForeignKey(Vendor, null=True)
    category = TreeForeignKey(Category, null=True)
    barcode_pdf417 = models.ImageField(upload_to="product_pdf417/", null=True, blank=True)

    weight_product = models.DecimalField(_("Product Weight"), help_text="In Ounces",
            max_digits=10, decimal_places=2, blank=True, default=0)
    weight_shipping = models.DecimalField(_("Shipping Weight"), help_text="In Ounces",
            max_digits=10, decimal_places=2, blank=True, default=0)

    dimension_height = models.DecimalField(_("Product Height"), help_text="In Inches",
            max_digits=10, decimal_places=2, blank=True, default=0)
    dimension_width = models.DecimalField(_("Product Width"), help_text="In Inches",
            max_digits=10, decimal_places=2, blank=True, default=0)
    dimension_depth = models.DecimalField(_("Product Depth"), help_text="In Inches",
            max_digits=10, decimal_places=2, blank=True, default=0)

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

        """
        Parses a string representing a GTIN in any of its formats
        and returns a normalised id. Throws a validation error if there
        is a problem.
        """
        VALID_GTIN_LENGTHS = [8, 12, 13, 14]

        # Remove everything except digits.
        # Could do this with regex, but this is simpler.
        nums = [ int(s) for s in self.gtin_id if s.isdigit() ]
        if not ( len(nums) in VALID_GTIN_LENGTHS ):
            raise ValidationError(_("This is not a valid length for a GTIN."))
        self.gtin_id = ''.join([str(n) for n in nums])

        super(Product, self).save(*args, **kwargs)

        # Generate the barcode using CandyBar.
        # Note: django-cleanup handles deleting the file if variant is deleted.
        if not self.barcode_pdf417:
            pdf417 = CandyBarPdf417()
            barcode_bytestring = pdf417.encode(self.get_sku())
            filename = "{}.png".format(
                os.path.join(
                    settings.MEDIA_ROOT, 'product_pdf417', self.get_sku() ))
            self.barcode_pdf417.save(filename, ContentFile(barcode_bytestring))
            self.save()

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
    asin_id = models.CharField(_("ASIN"), max_length=10, default="", blank=True,
                               help_text=_("Amazon Standard ID Number"))

    barcode_pdf417 = models.ImageField(upload_to="product_pdf417/", null=True, blank=True)

    weight_product = models.DecimalField(_("Product Weight"), help_text="In Ounces",
            max_digits=10, decimal_places=2, blank=True, default=0)
    weight_shipping = models.DecimalField(_("Shipping Weight"), help_text="In Ounces",
            max_digits=10, decimal_places=2, blank=True, default=0)

    dimension_height = models.DecimalField(_("Product Height"), help_text="In Inches",
            max_digits=10, decimal_places=2, blank=True, default=0)
    dimension_width = models.DecimalField(_("Product Width"), help_text="In Inches",
            max_digits=10, decimal_places=2, blank=True, default=0)
    dimension_depth = models.DecimalField(_("Product Depth"), help_text="In Inches",
            max_digits=10, decimal_places=2, blank=True, default=0)

    def get_sku(self):
        rv = "{}-{}".format(self.product.get_sku(), self.code)
        return rv
    get_sku.short_description = _("Variant SKU")

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):


        """
        Parses a string representing a GTIN in any of its formats
        and returns a normalised id. Throws a validation error if there
        is a problem.
        """
        VALID_GTIN_LENGTHS = [8, 12, 13, 14]

        # Remove everything except digits.
        # Could do this with regex, but this is simpler.
        nums = [ int(s) for s in self.gtin_id if s.isdigit() ]
        if not ( len(nums) in VALID_GTIN_LENGTHS ):
            raise ValidationError(_("This is not a valid length for a GTIN."))
        self.gtin_id = ''.join([str(n) for n in nums])

        super(ProductVariant, self).save(*args, **kwargs)

        # Generate the barcode using CandyBar.
        # Note: django-cleanup handles deleting the file if variant is deleted.
        if not self.barcode_pdf417:
            pdf417 = CandyBarPdf417()
            barcode_bytestring = pdf417.encode(self.get_sku())
            filename = "{}.png".format(
                os.path.join(
                    settings.MEDIA_ROOT, 'product_pdf417', self.get_sku() ))
            self.barcode_pdf417.save(filename, ContentFile(barcode_bytestring))
            self.save()

    class Meta:
        verbose_name = "Variant"
        verbose_name_plural = "Variants"
