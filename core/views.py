from django.shortcuts import render
from core.models import Product



def home(request):
    most_cheap_products = Product.objects.get_most_cheap_products()
    new_products = Product.objects.get_new_products() #Выводит последние 3 товара за последние 7 дней

    return render(request, "core/home.html", {
        "new_products": new_products,
        "most_cheap_products": most_cheap_products
    })

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "core/product_detail.html", {
        "product": product
    })