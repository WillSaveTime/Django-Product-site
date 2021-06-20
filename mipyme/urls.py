"""mipyme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .views import home_view, LoginView, logout_view
from pymes.views import select_pyme_view, DashboardHomeView
from products.views import ProductsView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home_view, name="home"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", logout_view, name="logout"),

    path("select_pyme", select_pyme_view, name="select-pyme"),

    path("<str:pyme_code>/dashboard/home", DashboardHomeView.as_view(), name="dashboard-home"),
    path("<str:pyme_code>/dashboard/products", ProductsView.as_view(), name="dashboard-products"),
    path("<str:pyme_code>/dashboard/products/edit/<int:product_id>", ProductsView.as_view(), name="edit-product"),
    #path("<str:pyme_code>/dashboard/orders", name="dashboard-orders"),

    path("product", include("products.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
