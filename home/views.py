from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Customer
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from products.models import Product


def index(request):
    return render(request, "home/index.html")


# Shop View
@login_required
def shop(request):
    products = Product.objects.all()
    return render(request, 'home/products.html', {'products': products})


# View to show Customer profile
@login_required
def customer_profile(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, "home/customer_profile.html", {"customer": customer})


@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer # Assuming user is logged in
            # if the user didn't provide a delivery address, use their primary address
            if not order.delivery_address:
                order.delivery_address = request.user.customer.address
            order.save()
            return redirect("home:product_list")
    else:
        form = OrderForm()
    return render(request, "home/order_form.html", {"form": form})


def our_story(request):
    return render(request, 'home/our_story.html')

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})



