from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .cart import Cart
from .forms import CheckoutForm, SignUpForm
from .models import Order, OrderItem, Product

def home(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "store/home.html", {"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "store/product_detail.html", {"product": product})

def cart_detail(request):
    return render(request, "store/cart.html", {"cart": Cart(request)})

def cart_add(request, product_id):
    if request.method != "POST":
        return redirect("store:home")
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get("quantity", 1))
    if quantity < 1 or product.stock < 1:
        messages.error(request, "This product is currently unavailable.")
    else:
        Cart(request).add(product, quantity)
        messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.META.get("HTTP_REFERER", "store:home"))

def cart_remove(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        Cart(request).remove(product)
        messages.info(request, "Item removed from your cart.")
    return redirect("store:cart_detail")

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Your cart is empty.")
        return redirect("store:home")
    initial = {"full_name": request.user.get_full_name() or request.user.username,
               "email": request.user.email}
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                items = list(cart)
                for item in items:
                    product = Product.objects.select_for_update().get(pk=item["product"].pk)
                    if product.stock < item["quantity"]:
                        messages.error(request, f"Not enough stock for {product.name}.")
                        return redirect("store:cart_detail")
                order = Order.objects.create(user=request.user, total=cart.get_total_price(), **form.cleaned_data)
                for item in items:
                    product = Product.objects.select_for_update().get(pk=item["product"].pk)
                    OrderItem.objects.create(order=order, product=product,
                        product_name=product.name, unit_price=product.price, quantity=item["quantity"])
                    product.stock -= item["quantity"]
                    product.save(update_fields=["stock"])
                cart.clear()
            return redirect("store:order_success", order_id=order.id)
    else:
        form = CheckoutForm(initial=initial)
    return render(request, "store/checkout.html", {"form": form, "cart": cart})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "store/order_success.html", {"order": order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "store/my_orders.html", {"orders": orders})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created.")
            return redirect("store:home")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})
