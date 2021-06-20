from django.contrib.messages.api import MessageFailure
from django.db.models.expressions import Value
import products
from django.http import request
from django.shortcuts import redirect, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import TemplateView

from .models import Product, ProductPicture, ProductCategory, ProductManufacturingDetails, ProductSpecification, ProductSubCategory
from .forms import ProductForm

from pymes.views import PymeAuthView
from pymes.models import PymeUser

from django.contrib import messages

PAGE_SIZE = 10

import json


class ProductsView(PymeAuthView):
    template_path = "dashboard/products/products.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        page = request.GET.get("page")
        sortByParams = request.GET.get("sortBy")
        search = request.GET.get("search")

        products = self.pyme.products.active()

        # todo: redo search to work with django's filters
        # if search and search != "":
        #     search_results = []
        #     for product in products:
        #         for key in prod:
        #             value = str(prod[key]).lower()
        #             if search.lower() in value:
        #                 search_results.append(prod)
        #                 break

        #     prods = search_results

        if sortByParams:
            sortBy = sortByParams.split("-")[0]
            order = sortByParams.split("-")[1]
            if order == "Asc":
                descending = False
            elif order == "Des":
                descending = True
            else:
                descending = False

            sortByParam = lambda element: element[sortBy]
            products.sort(reverse=descending, key=sortByParam)

        products_paginator = Paginator(products, PAGE_SIZE)
        try:
            products = products_paginator.page(page)
        except PageNotAnInteger:
            products = products_paginator.page(1)
        except EmptyPage:
            products = products_paginator.page(products_paginator.num_pages)
        # Context for prod data

        product_form = ProductForm()

        context = {
            "pyme" : self.pyme,
            "products": products,
            "product_form": product_form,
            "productCategories":ProductCategory.objects.all(),
            "productSpecification":ProductSpecification.objects.all(),
            "productSubCategory":ProductSubCategory.objects.all(),
            "productManufacturingDetails":ProductManufacturingDetails.objects.all(),
        }
        return render(request, self.template_path, context=context)


# Function that show warning and redirect to given url
def showWarningAndRedirect(request, warning, redirectUrl):
    messages.warning(request, warning)
    return redirect(redirectUrl)

def addProduct(request):
    if request.method == 'POST':
        form_data = request.POST
        product_name = form_data.get("name")
        product_base_price = form_data.get("base_price")
        product_description = form_data.get("description")
        
        error = False

        category = request.POST["category"]
        category2 = request.POST["category2"]
        redirectUrl = f"/{PymeUser.objects.get(user=request.user).pyme.code}/dashboard/products"
        subcategory = request.POST["subcategory"]

        if request.POST["name"] == "":
            return showWarningAndRedirect(request, "Por favor ingrese el nombre", redirectUrl)

        if request.POST["specificationKey"] == "":
            return showWarningAndRedirect(request, "por favor ingrese las especificaciones", redirectUrl)
        
        if request.POST["base_price"] == "":
            return showWarningAndRedirect(request, "Ingrese el precio base", redirectUrl)
            
        
        if request.POST["base_price"] != "":
            try:
                int(request.POST["base_price"])
            except ValueError as e:
                return showWarningAndRedirect(request, "Ingrese un precio base válido", redirectUrl)
                
                
        if request.POST["description"] == "":
            return showWarningAndRedirect(request, "Por favor ingrese una descripción", redirectUrl)
            

        if request.POST["category"] == "":
            return showWarningAndRedirect(request, "Ingrese la primera categoría principal", redirectUrl)
            

        if request.POST["subcategory"] == "":
            return showWarningAndRedirect(request, "Por favor ingrese la subcategoría", redirectUrl)
            



        if request.POST["category2"] == "":
            return showWarningAndRedirect(request, "Ingrese la segunda categoría principal", redirectUrl)
            

        if "photo1" not in request.FILES:
            return showWarningAndRedirect(request, "Elija la primera foto", redirectUrl)
            

        if "photo2" not in request.FILES:
            return showWarningAndRedirect(request, "Elija la segunda foto", redirectUrl)
            

        if request.POST["base_cost"] == "":
            return showWarningAndRedirect(request, "Ingrese el costo base", redirectUrl)
            

        if request.POST["estimated_days"] == "":
            return showWarningAndRedirect(request, "Ingrese los días estimados", redirectUrl)
            

        if request.POST["requirements"] == "":
            return showWarningAndRedirect(request, "Ingrese los requisitos", redirectUrl)
            

        if request.POST["instructions"] == "":
            return showWarningAndRedirect(request, "Por favor ingrese las instrucciones", redirectUrl)
            

        else:
            pymeuser = PymeUser.objects.get(user=request.user)
            product = Product.objects.create(
                pyme=pymeuser.pyme,
                name=product_name,
                base_price=product_base_price,
                description=product_description,
            )
            

            productPicture = ProductPicture(product=product, picture=request.FILES['photo1'])
            productPicture.save()

            productPicture2 = ProductPicture(product=product, picture=request.FILES['photo2'])
            productPicture2.save()

            productCategory = ProductCategory(name=json.dumps({"category1":request.POST["category"], "category2":request.POST["category2"], "productId":product.id}))
            productCategory.save()

            productSubCategory = ProductSubCategory(name=request.POST["subcategory"], category=productCategory)
            productSubCategory.save()

            product.subcategory = productSubCategory

            productSpecification = ProductSpecification(key=request.POST["specificationKey"], product=product)
            productSpecification.save()

            productManufacturingDetails = ProductManufacturingDetails(product=product, base_cost=request.POST["base_cost"], estimated_days=request.POST["estimated_days"], requirements=request.POST["requirements"], instructions=request.POST["instructions"])
            productManufacturingDetails.save()

            product.save()

            return redirect(f"/{pymeuser.pyme.code}/dashboard/products")

    else:
        return HttpResponse("404 Not Found!")

# To edit the product
def editProduct(request):
    if request.method == "POST":
        productId = request.POST["productId"]

        # Get the product
        product = Product.objects.get(id=productId)
        productManufacturingDetails = ProductManufacturingDetails.objects.get(product=product)
        productPicture = ProductPicture.objects.filter(product=product)
        productsCategories = ProductCategory.objects.all()
        for item in productsCategories:
            if json.loads(item.name)["productId"] == product.id:
                productCategory = item

        itemsDict = dict(request.POST)
        del itemsDict["csrfmiddlewaretoken"]
        del itemsDict["productId"]

        redirectUrl = f"/{PymeUser.objects.get(user=request.user).pyme.code}/dashboard/products"

        print(request.POST)

        
        newname = request.POST["newname"]
        newbase_price = request.POST["newbase_price"]
        newdescription = request.POST["newdescription"]
        newcategory = request.POST["newcategory"]
        newcategory2 = request.POST["newcategory2"]
        # newphoto1 = request.FILES["newphoto1"]
        # newphoto2 = request.FILES["newphoto2"]
        newbase_cost = request.POST["newbase_cost"]
        newestimated_days = request.POST["newestimated_days"]
        newrequirements = request.POST["newrequirements"]
        newinstructions = request.POST["newinstructions"]
        newspecificationKey = request.POST["newspecificationKey"]
        newsubcategory = request.POST["newsubcategory"]

        if newcategory != "" and newcategory2 != "":
            productCategory.category = json.dumps({"category1":newcategory, "category2":newcategory2, "productId":product.id})

        elif newcategory == "" and newcategory2 != "":
            initialNewCat1 = json.loads(productCategory.name)["category1"]
            productCategory.category = json.dumps({"category1":initialNewCat1, "category2":newcategory2, "productId":product.id})

        elif newcategory != "" and newcategory2 == "":
            initialNewCat2 = json.loads(productCategory.name)["category2"]
            productCategory.category = json.dumps({"category1":newcategory, "category2":initialNewCat2, "productId":product.id})



        if newname != "":
            product.name = newname


        if newbase_price != "":
            product.base_price = newbase_price

        if newdescription != "":
            product.description = newdescription

        if newbase_cost != "":
            productManufacturingDetails.base_cost = newbase_cost

        if newestimated_days != "":
            productManufacturingDetails.estimated_days = newestimated_days

        if newrequirements != "":
            productManufacturingDetails.requirements = newrequirements

        if newinstructions != "":
            productManufacturingDetails.instructions = newinstructions

        if "newphoto1" in request.FILES:
            productPicture[0].picture = request.FILES["newphoto1"]

        if "newphoto2" in request.FILES:
            productPicture[1].picture = request.FILES["newphoto2"]

        if newspecificationKey != "":
            productSpecification = ProductSpecification.objects.get(product=product)
            productSpecification.key = newspecificationKey
            productSpecification.save()

        product.save()
        productManufacturingDetails.save()
        # productPicture.save()


        # print("Log from editProduct", itemsDict, product)
        # Redirect user to products dahsboard
        return redirect(f"/{product.pyme.code}/dashboard/products")

def deleteProduct(request):
    if request.method == "POST":
        productId = request.POST["productId"]

        product = Product.objects.get(id=productId)
        product.delete()
        product.save()
        return redirect(f"/{product.pyme.code}/dashboard/products")

def getProductImages(request):
    if request.method == "POST":
        product = Product.objects.get(id=json.loads(request.body)["productId"])
        productPicture = ProductPicture.objects.filter(product=product)

        picturesList = []

        for item in productPicture:
            picturesList.append(str(item.picture))

        
        return HttpResponse(json.dumps(picturesList))