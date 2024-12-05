# shop/views.py
from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Order

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def cart(request):
    orders = Order.objects.filter(user=request.user, ordered=False)
    return render(request, 'cart.html', {'orders': orders})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    Order.objects.create(user=request.user, product=product, quantity=1)
    return redirect('cart')

@login_required
def checkout(request):
    orders = Order.objects.filter(user=request.user, ordered=False)
    for order in orders:
        order.ordered = True
        order.save()
    return redirect('home')
