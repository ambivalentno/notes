from forms import NewNoteForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from notes.models import Note


def index(request):
    context = {'notes': Note.objects.all()}
    return render(request, 'index.html', context)


def add_note(request):
    form = NewNoteForm(attrs=request.POST or None)
    if form.is_valid():
        note = Note(title=form.cleaned_data['title'],
         text=form.cleaned_data['text'])
        note.save()
        if request.is_ajax():
            return render(request, 'ajax_success.html', {'form': NewNoteForm()})
        return HttpResponseRedirect('/')
    if request.is_ajax():
        return render(request, 'ajax_fail.html', {'form': form}) 
    return render(request, 'add_note.html', {'form': form})


def count(request):
    form1 = NewNoteForm(formname='test')
    form2 = NewNoteForm(formname='test2')
    return render(request, 'count.html', {'forms': [form1, form2]})
