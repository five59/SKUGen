from django.contrib import admin
from .models import *

class BrandInline(admin.TabularInline):
    model = Brand
    extra = 1

class VendorInline(admin.TabularInline):
    model = Vendor
    extra = 1

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

class VariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class BrandAdmin(admin.ModelAdmin):
    inlines = (ProductInline, )

class VendorAdmin(admin.ModelAdmin):
    inlines = (ProductInline, )

class CategoryAdmin(admin.ModelAdmin):
    inlines = (ProductInline, )

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'get_sku', 'get_numvariants',
    )
    list_filter = (
        ('category', admin.RelatedOnlyFieldListFilter),
        ('vendor', admin.RelatedOnlyFieldListFilter),
        ('brand', admin.RelatedOnlyFieldListFilter),
    )
    inlines = (VariantInline, )


admin.site.register(Brand, BrandAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)