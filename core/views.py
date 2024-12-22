from django.shortcuts import render
from core.models import Flight


def index(request):
    flights = Flight.objects.all().select_related('status').order_by('-id')
    return render(request, 'index.html', {'flights': flights})