from django.shortcuts import get_object_or_404, render, redirect

def index(request):
    """ Redirect to the polls index"""
    return redirect("polls:index")
