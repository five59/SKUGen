from django.shortcuts import render
from candybar.CandyBarPdf417 import CandyBarPdf417
from django.http import HttpResponse
from django.template import loader
from .models import *

def all_barcodes(request):
    products = Product.objects.all()
    context = { 'products': products }
    return render(request, 'catalog/bars.html', context)
