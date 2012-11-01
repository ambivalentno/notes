# Create your views here.
from django.shortcuts import render
from notes.models import Note


def index(request):
    context = {'notes': Note.objects.all()}
    return render(request, 'index.html', context)
