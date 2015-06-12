from django.shortcuts import render, redirect
from django.http import HttpResponse


def about(request):
    return render(request, 'about.html')
