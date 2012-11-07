from forms import NewNoteForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from notes.models import Note



def index(request):
    context = {'notes': Note.objects.all()}
    return render(request, 'index.html', context)

def add_note(request):
	if request.method == 'POST':
		form = NewNoteForm(data=request.POST)
		print request.POST
		print form.errors
		if form.is_valid():
			note = Note(title=form.cleaned_data['title'], text=form.cleaned_data['text'][0])
			#note.save()
			return HttpResponseRedirect('/')
	else:
		form = NewNoteForm(data={'form_name':'add_note'})
	return render(request, 'add_note.html', {'form' : form})

def count(request):
	form1 = NewNoteForm(data={'form_name':'test'})
	form2 = NewNoteForm(data={'form_name':'test2'})
	return render(request, 'count.html', {'forms' : [form1,form2]})
