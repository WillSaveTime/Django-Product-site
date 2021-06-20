from django.contrib import admin
from django.urls import path, include

from products import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("/getProductImages", views.getProductImages, name="getProductImages"),
    path("/addProduct", views.addProduct, name="addProduct"),
    path("/edit", views.editProduct, name="editProduct"),
    path("/delete", views.deleteProduct, name="deleteProduct"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)