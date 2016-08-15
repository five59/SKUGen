from django.shortcuts import render
from candybar.CandyBarPdf417 import CandyBarPdf417
from django.http import HttpResponse
from django.template import loader
from .models import *

def all_barcodes(request):
    variants = ProductVariant.objects.all()
    context = { 'v': variants }
    return render(request, 'catalog/bars.html', context)
