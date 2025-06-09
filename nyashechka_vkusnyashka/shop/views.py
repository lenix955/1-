from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q, Count
from .models import Product, Promotion, Category, Review, CartItem
from .forms import SearchForm, ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import random

def home(request):
    now = timezone.now()
    recent_date = now - timedelta(days=30)
    new_products = Product.objects.filter(is_available=True).order_by('-created_at')[:5]
    active_promotions = Promotion.objects.filter(
        start_date__lte=now.date(),
        end_date__gte=now.date()
    ).order_by('-start_date')[:5]
    top_categories = Category.objects.annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0).order_by('-product_count')[:3]
    if top_categories.count() < 3:
        random_categories = list(Category.objects.exclude(id__in=top_categories.values_list('id', flat=True)))
        random.shuffle(random_categories)
        top_categories = list(top_categories) + random_categories[:3 - top_categories.count()]
    form = SearchForm(request.GET or None)
    search_results = []
    if form.is_valid() and form.cleaned_data['query']:
        query = form.cleaned_data['query']
        search_results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()
    products_with_cart = []
    for product in new_products:
        products_with_cart.append({
            'product': product,
            'in_cart': CartItem.objects.filter(user=request.user, product=product).exists() if request.user.is_authenticated else False,
            'is_new': product.created_at > recent_date,
        })
    return render(request, 'shop/home.html', {
        'new_products': products_with_cart,
        'active_promotions': active_promotions,
        'top_categories': top_categories,
        'form': form,
        'search_results': search_results,
        'recent_date': recent_date,
    })

def search(request):
    form = SearchForm(request.GET or None)
    results = []
    query = ''
    now = timezone.now()
    recent_date = now - timedelta(days=30)
    if form.is_valid() and form.cleaned_data.get('query'):
        query = form.cleaned_data['query']
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()
        products_with_cart = []
        for product in results:
            products_with_cart.append({
                'product': product,
                'in_cart': CartItem.objects.filter(user=request.user, product=product).exists() if request.user.is_authenticated else False,
                'is_new': product.created_at > recent_date,
            })
        results = products_with_cart
    return render(request, 'shop/search.html', {
        'results': results,
        'query': query,
        'form': form,
        'recent_date': recent_date,
    })

def promotions(request):
    now = timezone.now().date()
    past_promotions = Promotion.objects.filter(end_date__lt=now).order_by('-end_date')
    active_promotions = Promotion.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    ).order_by('-start_date')
    future_promotions = Promotion.objects.filter(start_date__gt=now).order_by('start_date')
    return render(request, 'shop/promotions.html', {
        'past_promotions': past_promotions,
        'active_promotions': active_promotions,
        'future_promotions': future_promotions,
    })

def catalog(request):
    now = timezone.now()
    recent_date = now - timedelta(days=30)
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if selected_category:
        products = products.filter(category_id=selected_category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    products_with_cart = []
    for product in products:
        products_with_cart.append({
            'product': product,
            'in_cart': CartItem.objects.filter(user=request.user, product=product).exists() if request.user.is_authenticated else False,
            'is_new': False,  # Плашка «Новинка» не нужна в каталоге
        })
    return render(request, 'shop/catalog.html', {
        'products': products_with_cart,
        'categories': categories,
        'selected_category': selected_category,
        'min_price': min_price,
        'max_price': max_price,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.order_by('-created_at')
    now = timezone.now()
    recent_date = now - timedelta(days=30)
    in_cart = CartItem.objects.filter(user=request.user, product=product).exists() if request.user.is_authenticated else False
    is_new = product.created_at > recent_date
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'in_cart': in_cart,
        'is_new': is_new,
    })

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.delete()
        messages.success(request, f"Товар '{product.name}' удалён из корзины!")
    else:
        messages.success(request, f"Товар '{product.name}' добавлен в корзину!")
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_detail'), pk=pk)

@login_required
def cart_list(request):
    cart_items = CartItem.objects.filter(user=request.user).order_by('-added_at')
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
    })

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Товар '{product.name}' создан!")
            return redirect('shop:catalog')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Добавить товар'})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Товар '{product.name}' обновлён!")
            return redirect('shop:catalog')
    form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Редактировать товар'})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Товар '{product_name}' удалён!")
        return redirect('shop:catalog')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})