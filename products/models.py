from django.db import models

from core.models import BaseModel
from pymes.models import Pyme
import json

class ProductCategory(BaseModel):
    name = models.CharField(
        max_length=70,
        blank=False,
        db_index=True)

    def add_others_subcategory(self):
        other_subcategory = ProductSubCategory(
            name="Otros",
            category=self)
        other_subcategory.save()

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def save(self, *args, **kwargs):
        if (not self.id):
            super(ProductCategory, self).save(*args, **kwargs)
            self.add_others_subcategory()

    def __str__(self):
        return f'{self.name}'


class ProductSubCategory(BaseModel):
    name = models.CharField(
        max_length=70,
        blank=False,
        db_index=True)
    category = models.ForeignKey(
        ProductCategory,
        related_name="subcategories",
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Product SubCategory"
        verbose_name_plural = "Product SubCategories"

    def __str__(self):
        return f'{self.name}'


class Product(BaseModel):
    pyme = models.ForeignKey(
        Pyme,
        related_name="products",
        on_delete=models.CASCADE)
    # Information
    name = models.CharField(
        max_length=75,
        blank=False,
        db_index=True)
    base_price = models.IntegerField(
        null=True)
    description = models.TextField(
        max_length=500,
        blank=True)
    # Category
    subcategory = models.ForeignKey(
        ProductSubCategory,
        related_name="products",
        null=True,
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    @property
    def category(self):
        return json.loads(self.subcategory.category.name)["category1"] if self.subcategory else None



    def __str__(self):
        return f'{self.name}'


class ProductSpecification(BaseModel):
    key = models.CharField(
        max_length=75,
        blank=False,
        db_index=True)
    product = models.ForeignKey(
        Product,
        related_name="specifications",
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Product Specifications"
    
    def __str__(self):
        return self.key


class ProductPicture(BaseModel):
    # todo: add base file model
    product = models.ForeignKey(
        Product,
        related_name="pictures",
        on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="productImages")

    class Meta:
        verbose_name = "Product Picture"
        verbose_name_plural = "Product Pictures"


class ProductManufacturingDetails(BaseModel):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE)
    base_cost = models.IntegerField(
        null=True)
    estimated_days = models.IntegerField(
        null=True)
    requirements = models.TextField(
        max_length=500,
        blank=True)
    instructions = models.TextField(
        max_length=500,
        blank=True)

    class Meta:
        verbose_name = "Product Manufacturing Details"
        verbose_name_plural = "Product Manufacturing Details"


class ProductStock(BaseModel):
    product = models.ForeignKey(
        Product,
        related_name="stock",
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Product Stock"
        verbose_name_plural = "Product Inventory"


class ProductStockSpecification(BaseModel):
    specification = models.ForeignKey(
        ProductSpecification,
        related_name="+",
        on_delete=models.CASCADE)
    product_stock = models.ForeignKey(
        ProductStock,
        related_name="specifications",
        on_delete=models.CASCADE)
    value = models.CharField(
        max_length=75,
        blank=False)

    class Meta:
        verbose_name = "Product Stock Specification"
        verbose_name_plural = "Product Stock Specifications"