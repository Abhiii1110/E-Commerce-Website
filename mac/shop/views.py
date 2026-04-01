from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Product , Order , OrderItem
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def index(request):
    
    products = Product.objects.all()
    paginator = Paginator(products,8)
    page_number = request.GET.get('page')
    prodfinal = paginator.get_page(page_number)
    totalpage=prodfinal.paginator.num_pages
    data = {
        'products': prodfinal,
        'lastpage': totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
    }
    return render(request, 'shop/index.html', data)

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(category__icontains=query) |
            Q(subcategory__icontains=query)
        )

    return render(request, 'shop/index.html', {'products': products, 'query': query})

def productView(request,product_id):
    prodview = get_object_or_404(Product, id= product_id )
    return render(request, 'shop/productView.html', {"prodView":prodview})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart') 

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    total_amount = 0
    order_items = []

    for product in products:
        quantity = cart[str(product.id)]
        price = product.price
        total_price = price * quantity
        total_amount += total_price

        order_items.append({
            'product': product,
            'quantity': quantity,
            'price': price,
        })

    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount
    )
    for item in order_items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price'],
        )
    request.session['cart'] = {}
    return render(request, 'shop/checkout.html',{'order': order})


def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'shop/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['confirm_password']

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)  
        return redirect('index')  
    return render(request, 'shop/signup.html')


def user_logout(request):
    logout(request)
    return redirect('index')


def addtocart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    cart_items = []
    for product in products:
        quantity = cart[str(product.id)]
        total_price = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })

    context = {'cart_items': cart_items}
    return render(request, 'shop/cart.html', context)


def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
        request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            cart.pop(str(product_id))
        request.session['cart'] = cart
    return redirect('cart')


def TermsNConditions(request):
    return render(request, 'shop/terms.html')

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')




