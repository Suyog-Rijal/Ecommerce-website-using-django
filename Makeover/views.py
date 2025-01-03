from decimal import Decimal

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from . import models


def home(request):
    context = {}

    flash_sales = models.Product.objects.all()[:6]
    product_of_the_day = models.Product.objects.all()[6:12]
    best_beauty_products = [
        'bobbi.jpg',
        'lakme.jpg',
        'loreal.png',
        'tiege.png',
        'clinique.jpeg',
        'dove.png',
        'nukaa.jpg',
        'ponds.png',
    ]
    attractive_accessories = models.Product.objects.all()[12:18]
    best_outfits = models.Product.objects.all()[18:22]

    context['flash_sales'] = flash_sales
    context['product_of_the_day'] = product_of_the_day
    context['best_beauty_products'] = best_beauty_products
    context['attractive_accessories'] = attractive_accessories
    context['best_outfits'] = best_outfits

    return render(request, 'home.html', context)


def products(request):
    category = request.GET.get('category')
    shortBy = request.GET.get('shortBy')
    context = {}

    data = models.Product.objects.all()
    if category:
        if category == 'Offers':
            data = data.filter(discount_percent__gt=0)
            context['category'] = 'Offers'
        else:
            data = data.filter(category__name=category)
            context['category'] = category

    if shortBy:
        pass

    context['data'] = data
    return render(request, 'products.html', context)


def search(request):
    query = request.GET['data']
    response = models.Product.objects.filter(Q(short_name__icontains=query) | Q(full_name__icontains=query))
    return JsonResponse(list(response.values()), safe=False)


def product_detail(request, product_id=None):
    if product_id:
        data = models.Product.objects.get(id=product_id)
        return render(request, 'productDetail.html', {'data': data})
    return render(request, 'productDetail.html')


def cart_view(request):
    return render(request, 'cart.html')

