from django.shortcuts import render, redirect
from django.http import HttpResponse

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')
