from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Member, Product
from .forms import ProductForm
from .forms import MemberForm
from django.conf import settings
import os

def home(request):
    all_products = Product.objects.all()[:10]  # Retrieve the first 10 products
    products_part1 = all_products[:5]  # Retrieve the first 5 products
    products_part2 = all_products[5:]  # Retrieve the remaining 5 products
    media_url = settings.MEDIA_URL
    context = {
        'media_url':media_url,
        'products_part1': products_part1,
        'products_part2': products_part2,
    }
    return render(request, 'myapp/home.html', context)

# produk
def product_list(request):
    products = Product.objects.all()
    return render(request, 'myapp/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'myapp/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'myapp/product_create.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'myapp/product_update.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        if product.image:
            product.image.delete()
        product.delete()
        return redirect('product_list')
    return render(request, 'myapp/product_delete.html', {'product': product})

# member
def member_list(request):
    members = Member.objects.all()
    return render(request, 'myapp/member_list.html', {'members': members})

def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    return render(request, 'myapp/member_detail.html', {'member': member})

def member_create(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm()
    return render(request, 'myapp/member_create.html', {'form': form})

def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_detail', pk=pk)
    else:
        form = MemberForm(instance=member)
    return render(request, 'myapp/member_update.html', {'form': form, 'member': member})

def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('member_list')
    return render(request, 'myapp/member_delete.html', {'member': member})