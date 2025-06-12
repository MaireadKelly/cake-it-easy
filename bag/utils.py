# bag/utils.py
from decimal import Decimal
from django.conf import settings
from products.models import ProductVariant, Accessory, Product


def get_bag_contents(session):
    bag = session.get('bag', {})
    items = []
    total = Decimal('0.00')

    for key, item in bag.items():
        try:
            product = Product.objects.get(id=item['product_id'])
            variant = ProductVariant.objects.get(id=item['variant_id'])
            accessories = Accessory.objects.filter(id__in=item.get('accessory_ids', []))
        except (Product.DoesNotExist, ProductVariant.DoesNotExist):
            continue

        accessory_total = sum(a.price for a in accessories)
        subtotal = (variant.price + accessory_total) * item['quantity']

        items.append({
            'key': key,
            'product': product,
            'variant': variant,
            'accessories': accessories,
            'quantity': item['quantity'],
            'subtotal': subtotal
        })
        total += subtotal

    return {
        'items': items,
        'total': total,
    }


def add_to_bag(session, product_id, variant_id, accessory_ids, quantity):
    bag = session.get('bag', {})
    key = f'{product_id}:{variant_id}:{"-".join(map(str, sorted(accessory_ids)))}'

    if key in bag:
        bag[key]['quantity'] += quantity
    else:
        bag[key] = {
            'product_id': product_id,
            'variant_id': variant_id,
            'accessory_ids': accessory_ids,
            'quantity': quantity,
        }

    session['bag'] = bag
    session.modified = True
    return key


def update_bag(session, key, quantity):
    bag = session.get('bag', {})
    if key in bag:
        bag[key]['quantity'] = quantity
        session['bag'] = bag
        session.modified = True


def remove_from_bag(session, key):
    bag = session.get('bag', {})
    if key in bag:
        del bag[key]
        session['bag'] = bag
        session.modified = True