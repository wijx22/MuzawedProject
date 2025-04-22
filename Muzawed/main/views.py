from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

def index_view(request):
    return render(request, 'main/index.html')

# Create your views here.
