# /bag/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, ProductVariant, Accessory

def add_to_bag(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(Product, slug=slug)
        variant_id = request.POST.get('variant')
        accessory_ids = request.POST.getlist('accessories')
        quantity = int(request.POST.get('quantity', 1))

        bag = request.session.get('bag', {})
        key = f"{slug}-{variant_id}-{'-'.join(sorted(accessory_ids))}"

        if key in bag:
            bag[key]['quantity'] += quantity
        else:
            bag[key] = {
                'product': product.name,
                'variant': variant_id,
                'accessories': accessory_ids,
                'quantity': quantity,
            }

        request.session['bag'] = bag
        messages.success(request, f"Added {product.name} to your bag!")
        return redirect('product_detail', slug=slug)

def view_bag(request):
    bag = request.session.get('bag', {})
    items = []
    total = 0

    for key, item in bag.items():
        product = Product.objects.filter(name=item['product']).first()
        variant = ProductVariant.objects.filter(id=item['variant']).first()
        accessories = Accessory.objects.filter(id__in=item['accessories'])
        price = variant.price if variant else 0
        acc_total = sum(a.price for a in accessories)
        subtotal = (price + acc_total) * item['quantity']
        total += subtotal

        items.append({
            'key': key,
            'product': product,
            'variant': variant,
            'accessories': accessories,
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })

    return render(request, 'bag/bag.html', {'items': items, 'total': total})

def remove_from_bag(request, key):
    bag = request.session.get('bag', {})
    if key in bag:
        del bag[key]
        request.session['bag'] = bag
        messages.success(request, "Item removed from your bag.")
    return redirect('view_bag')

def update_quantity(request, key):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        bag = request.session.get('bag', {})
        if key in bag:
            bag[key]['quantity'] = quantity
            request.session['bag'] = bag
            messages.success(request, "Quantity updated.")
    return redirect('view_bag')