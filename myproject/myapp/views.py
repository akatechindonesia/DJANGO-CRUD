from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import Member, Product, Transaction, TransactionItem
from .forms import ProductForm
from .forms import MemberForm
from .forms import LoginForm
from datetime import datetime

import json
import requests
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

def product_buying(request):
    products = Product.objects.all()
    return render(request, 'myapp/product_buying.html', {'products': products})

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')        
        product_name = request.POST.get('product_name')        
        product_price = request.POST.get('product_price')        

        if 'cart' in request.session:
            request.session['cart'].append((product_id, product_name, product_price))
        else:
            request.session['cart'] = [(product_id, product_name, product_price)]
        
        request.session.modified = True
        return redirect('product_buying')
    products = Product.objects.all()
    return render(request, 'myapp/product_buying.html', {'products': products})

def remove_from_cart(request, item_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        for item in cart:
            if item[0] == str(item_id):
                cart.remove(item)
                break
        request.session['cart'] = cart
        request.session.modified = True
    products = Product.objects.all()
    return render(request, 'myapp/product_buying.html', {'products': products, 'item_id': item_id})

def product_final_trans(request):
    cart = request.session.get('cart', [])
    member = request.POST.get('member')
    total_amount = request.POST.get('total_amount')
    product_item =  json.loads(request.POST.get('product_item')) 
    product_itemx =  request.POST.get('product_item')
    context = {
        'cart': cart,
        'member':member,
        'total_amount':total_amount,
        'product_item':product_item,
        'product_itemx':product_itemx,
    }
    return render(request, 'myapp/product_final_trans.html', context)

def product_buying_save(request):
    member_id = request.POST.get('member')
    total_amount = request.POST.get('total_amount')
    product_item = json.loads(request.POST.get('product_item'))

    transaction = Transaction.objects.create(member_id=member_id, total_amount=total_amount)

    for product_id, product_data in product_item.items():
        name = product_data['name']
        jumlah = product_data['jumlah']
        total = product_data['total']
        product = get_object_or_404(Product, id=product_id)
        TransactionItem.objects.create(transaction=transaction, product=product, quantity=jumlah, price=total)
    request.session.pop('cart', None)
    return redirect('history')

def history(request):
    user = request.user
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if user.is_authenticated and not user.is_staff and start_date:
        transactions = Transaction.objects.filter(purchase_date__range=(start_date, end_date))
        transaction_items = TransactionItem.objects.filter(transaction__in=transactions)
    
    if user.is_authenticated and user.is_staff:
        transactions = Transaction.objects.filter(member=user)
        transaction_items = TransactionItem.objects.filter(transaction__in=transactions)        

    if user.is_authenticated and not user.is_staff and not start_date:
        transactions = Transaction.objects.filter()
        transaction_items = TransactionItem.objects.filter(transaction__in=transactions)

    context = {
        'transactions': transactions,
        'transaction_items': transaction_items,
    }

    return render(request, 'myapp/history.html', context)


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

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the URL name of the main page after login
            else:
                form.add_error(None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
    else:
        form = LoginForm()
    return render(request, 'myapp/login_view.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def testing_api(request):
    response = requests.get('https://pokeapi.co/api/v2/berry')
    if response.status_code == 200:
        data = response.json()
        berries = data['results']
    else:
        berries = []

    context = {
        'berries': berries
    }

    return render(request, 'myapp/testing_api.html', context)