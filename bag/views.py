# bag/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, ProductVariant, Accessory
from .forms import AddToBagForm

def _get_bag(request):
    return request.session.get('bag', {})

def _save_bag(request, bag):
    request.session['bag'] = bag
    request.session.modified = True

def view_bag(request):
    bag = _get_bag(request)
    items = []
    total = 0

    for key, item in bag.items():
        product = get_object_or_404(Product, id=item['product_id'])
        variant = get_object_or_404(ProductVariant, id=item['variant_id'])
        accessories = Accessory.objects.filter(id__in=item['accessory_ids'])

        subtotal = variant.price + sum(a.price for a in accessories)
        subtotal *= item['quantity']
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

def add_to_bag(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = AddToBagForm(request.POST)
        if form.is_valid():
            variant = form.cleaned_data['variant']
            quantity = form.cleaned_data['quantity']
            accessories = form.cleaned_data['accessories']

            bag = _get_bag(request)
            key = f"{product_id}:{variant.id}:{'-'.join(str(a.id) for a in accessories)}"

            if key in bag:
                bag[key]['quantity'] += quantity
            else:
                bag[key] = {
                    'product_id': product_id,
                    'variant_id': variant.id,
                    'accessory_ids': [a.id for a in accessories],
                    'quantity': quantity
                }

            _save_bag(request, bag)
            messages.success(request, f"{product.name} added to your bag.")
            return redirect('view_bag')
        else:
            messages.error(request, "Invalid input. Please try again.")

    return redirect('product_detail', slug=product.slug)

def update_quantity(request, key):
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            bag = _get_bag(request)
            if key in bag:
                bag[key]['quantity'] = quantity
                _save_bag(request, bag)
                messages.success(request, "Quantity updated.")
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity.")
    return redirect('view_bag')

def remove_from_bag(request, key):
    if request.method == 'POST':
        bag = _get_bag(request)
        if key in bag:
            del bag[key]
            _save_bag(request, bag)
            messages.success(request, "Item removed from bag.")
    return redirect('view_bag')
