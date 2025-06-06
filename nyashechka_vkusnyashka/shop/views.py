from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Store
from django.http import HttpResponse

def index(request):
    return HttpResponse("Привет из 'Няшечка Вкусняшечка' 🎂")

def home(request):
    products = Product.objects.all().order_by('-created_at')[:12]  # последние 12 новинок
    return render(request, 'main/home.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'main/product_list.html', {'products': products, 'categories': categories})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'main/product_detail.html', {'product': product})


def about(request):
    return render(request, 'main/about.html')
