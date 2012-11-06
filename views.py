from forms import NewNoteForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from notes.models import Note



def index(request):
    context = {'notes': Note.objects.all()}
    return render(request, 'index.html', context)

def add_note(request):
	if request.method == 'POST':
		inpname = request.POST[u'form_name']
		form = NewNoteForm(request.POST, name=inpname)
		if form.is_valid():
			shared_name = form.cleaned_data['form_name']
			text_name = 'text'+shared_name+'_0' #created new name, as it changed after new widget creation
			note = Note(title=form.cleaned_data['title'], text=form.cleaned_data[text_name])
			note.save()
			return HttpResponseRedirect('/')
		else:
			print form.cleaned_data
	else:
		form = NewNoteForm(name='add_note')
	return render(request, 'add_note.html', {'form' : form})

def count(request):
	form1 = NewNoteForm(name='test')
	form2 = NewNoteForm(name='test2')
	return render(request, 'count.html', {'forms' : [form1,form2]})
