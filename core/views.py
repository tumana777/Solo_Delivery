from django.shortcuts import render

from core.models import ChinaAddress, USAAddress


def index(request):
    return render(request, 'index.html')