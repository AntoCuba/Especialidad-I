from django.shortcuts import render
from .models import Compra
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def realizar_compra(request):
    compra = compra.objects.all()
    return render(request, 'realizar_compra.html', {'compra': compra})