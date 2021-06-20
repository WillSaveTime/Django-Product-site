from django.contrib import admin

from core.admin import BaseModelAdmin, AUDIT_FIELDS
from .models import ProductCategory, ProductSubCategory, Product, ProductSpecification


class ProductSubCategoryTabularInline(admin.TabularInline):
    model = ProductSubCategory
    exclude = AUDIT_FIELDS

@admin.register(ProductCategory)
class ProductCategoryAdmin(BaseModelAdmin):
    inlines = (ProductSubCategoryTabularInline,)
    list_display = ('name',) + AUDIT_FIELDS


class ProductSpecificationTabularInline(admin.TabularInline):
    model = ProductSpecification
    exclude = AUDIT_FIELDS

@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    inlines = (ProductSpecificationTabularInline,)
    list_display = ('name', 'pyme', 'base_price', 'category', 'subcategory') + AUDIT_FIELDS
    list_filter = ('pyme', 'subcategory')
