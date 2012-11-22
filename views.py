from forms import NoteForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from notes.models import Note
from django.conf import settings


def index(request):
    context = {'notes': Note.objects.all()}
    return render(request, 'index.html', context)


def add_note(request):
    if request.method == 'POST':
        form = NoteForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return render(request, 'ajax_success.html', {'form': NoteForm()})
            return HttpResponseRedirect('/')
        if request.is_ajax():
            return render(request, 'ajax_fail.html', {'form': form}) 
        return render(request, 'add_note.html', {'form': form})
    form = NoteForm()
    return render(request, 'add_note.html', {'form': form})

def count(request):
    form1 = NoteForm(formname='test')
    form2 = NoteForm(formname='test2')
    return render(request, 'count.html', {'forms': [form1, form2]})
