# /products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, DietaryTag

def product_list(request):
    category_slug = request.GET.get('category')
    dietary_slug = request.GET.get('diet')

    products = Product.objects.all()
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if dietary_slug:
        products = products.filter(dietary_tags__slug=dietary_slug)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'dietary_tags': DietaryTag.objects.all()
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = product.variants.all()
    accessories = product.accessories.all()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'variants': variants,
        'accessories': accessories,
    })
