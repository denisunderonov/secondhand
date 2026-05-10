from django.shortcuts import render
from django.db.models import Max, Min
from core.models import Product, Category, Brand
from django.shortcuts import redirect


def home(request):
    most_cheap_products = Product.objects.get_most_cheap_products()
    new_products = Product.objects.get_new_products() #Выводит последние 3 товара за последние 7 дней

    return render(request, "core/home.html", {
        "new_products": new_products,
        "most_cheap_products": most_cheap_products
    })

def product_detail(request, pk):
    product = Product.objects.with_catalog_relations().get(pk=pk)
    return render(request, "core/product_detail.html", {
        "product": product
    })

def catalog(request):
    categories = Category.objects.get_products_count()
    products = Product.objects.with_catalog_relations().all()
    price_stats = Product.objects.aggregate(price_min=Min("price"), price_max=Max("price"))
    return render(request, "core/catalog.html", {
        "categories": categories,
        "products": products,
        "total_products_count": products.count(),
        "price_stats": price_stats,
    })

def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect("catalog")

def edit_product(request, pk):
    product = Product.objects.with_catalog_relations().get(pk=pk)
    brands = Brand.objects.all()
    return render(request, "core/edit_product.html", {
        "product": product,
        "brands": brands
    })

def update_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.name = request.POST.get("name")
    product.price = request.POST.get("price")
    product.brand = Brand.objects.get(id=request.POST.get("brand"))
    product.save()
    return redirect("product_detail", pk=product.pk)

def cat_category(request, pk):
    category = Category.objects.get(pk=pk)
    products = Product.objects.with_catalog_relations().filter(category=category)
    categories = Category.objects.get_products_count()
    return render(request, "core/cat_category.html", {
        "category": category,
        "products": products,
        "categories": categories,
        "total_products_count": Product.objects.count(),
    })