from django.shortcuts import render , redirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product
from .forms import RegisterForm
print("✅ TYPE OF render IS:", type(render))

# 🏠 Home view
def home(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'store/home.html', {
        'products': products,
        'cart_count': cart_count
    })
print("✅ TYPE OF render IS:", type(render))


# ➕ Add product to cart (using session)
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Product not found")

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

# 🛒 View cart
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    cart_items = []
    total = 0

    for pid, qty in cart.items():
        try:
            prod = Product.objects.get(id=int(pid))
            subtotal = prod.price * qty
            total += subtotal
            cart_items.append({
                'product': prod,
                'quantity': qty,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count
    })

# 👤 User registration
def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "✅ Registered successfully! Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

# 🔐 Login
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"🎉 Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "❌ Invalid credentials")

    return render(request, 'store/login.html')

# 🚪 Logout
def logout_user(request):
    logout(request)
    messages.success(request, "✅ You have been logged out.")
    return redirect('home')
