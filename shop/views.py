from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .models import Product, Order, OrderItem, Blog, Comment, Contact, Wishlist
from django.contrib.auth.models import User
from decimal import Decimal

def home(request):
    products = Product.objects.all()[:6]  # Show only 6 products on homepage
    featured_products = Product.objects.filter(is_featured=True)
    return render(request, 'shop/home.html', {
        'products': products,
        'featured_products': featured_products
    })

def shop(request):
    category = request.GET.get('category', '')
    products = Product.objects.all()
    
    if category:
        products = products.filter(category=category)
    
    context = {
        'products': products,
        'current_category': category
    }
    
    if request.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        context['wishlist_products'] = wishlist_products
    
    return render(request, 'shop/shop.html', context)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Your message has been sent!')
        return redirect('contact')
    return render(request, 'shop/contact.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.exclude(pk=pk)[:4]
    in_wishlist = False
    
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'in_wishlist': in_wishlist
    })

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
    
    if wishlist_item.exists():
        wishlist_item.delete()
        messages.success(request, f'{product.name} removed from your wishlist!')
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, f'{product.name} added to your wishlist!')
    
    return redirect(request.META.get('HTTP_REFERER', 'shop'))

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'shop/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def cart(request):
    cart_items = request.session.get('cart', {})
    products = []
    total = Decimal('0.00')
    
    for product_id, quantity in cart_items.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * Decimal(quantity)
        total += subtotal
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
    
    return render(request, 'shop/cart.html', {
        'cart_items': products,
        'total': total
    })

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))
        
        if str(product_id) in cart:
            cart[str(product_id)] += quantity
        else:
            cart[str(product_id)] = quantity
        
        request.session['cart'] = cart
        messages.success(request, 'Product added to cart successfully!')
    
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, 'Product removed from cart successfully!')
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = request.session.get('cart', {})
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    products = []
    subtotal = Decimal('0.00')
    
    for product_id, quantity in cart_items.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * Decimal(quantity)
        subtotal += item_total
        products.append({
            'product': product,
            'quantity': quantity,
            'total_price': item_total
        })
    
    # Calculate shipping fee
    shipping_fee = Decimal('0.00') if subtotal > 1500 else Decimal('100.00')
    
    # Calculate total
    total = subtotal + shipping_fee
    
    # Apply discount if total is above ₹2000
    discount = None
    if subtotal > 2000:
        discount = {
            'code': 'BULK20',
            'amount': (subtotal * Decimal('0.20')).quantize(Decimal('0.00'))
        }
        total -= discount['amount']
    
    context = {
        'cart_items': products,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'discount': discount,
        'total': total
    }
    
    if request.method == 'POST':
        # Handle payment processing here
        # Clear cart after successful payment
        request.session['cart'] = {}
        messages.success(request, 'Order placed successfully!')
        return redirect('home')
    
    return render(request, 'shop/checkout.html', context)

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'shop/blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'shop/blog_detail.html', {'blog': blog})

@login_required
def add_comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(blog=blog, user=request.user, content=content)
        messages.success(request, 'Comment added successfully!')
        return redirect('blog_detail', pk=pk)
    return redirect('blog_detail', pk=pk)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/profile.html', {'orders': orders})

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
