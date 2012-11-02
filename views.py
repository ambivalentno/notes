from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from notes.models import Note

class NewNoteForm(forms.Form):
	title = forms.CharField(max_length=50)
	text = forms.CharField(min_length=10)

def index(request):
    context = {'notes': Note.objects.all()}
    return render(request, 'index.html', context)

def add_note(request):
	if request.method == 'POST':
		form = NewNoteForm(request.POST)
		if form.is_valid():
			note = Note(title=form.cleaned_data['title'], text=form.cleaned_data['text'])
			note.save()
			return HttpResponseRedirect('/')
	else:
		form = NewNoteForm()
	return render(request, 'add_note.html', {'form' : form})
