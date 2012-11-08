from forms import NewNoteForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from notes.models import Note


def index(request):
    context = {'notes': Note.objects.all()}
    return render(request, 'index.html', context)


def add_note(request):
    form = NewNoteForm(attrs=request.POST or attrs={'form_name': 'add_note'})
    if form.is_valid():
            note = Note(title=form.cleaned_data['title'],
             text=form.cleaned_data['text'])
            note.save()
            return HttpResponseRedirect('/')
    return render(request, 'add_note.html', {'form': form})


def count(request):
    form1 = NewNoteForm(attrs={'form_name': 'test'})
    form2 = NewNoteForm(attrs={'form_name': 'test2'})
    return render(request, 'count.html', {'forms': [form1, form2]})
