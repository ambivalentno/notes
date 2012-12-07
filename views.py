'''Views for notes app'''
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from notes.models import Note
from notes.forms import NoteForm


def index(request):
    '''Shows list of all Note objects.'''
    context = {'notes': Note.objects.all(), 'site': request.get_host()}
    return render(request, 'index.html', context)


def add_note(request):
    '''Shows form to add note and processes its POST product.'''
    if request.method == 'POST':
        form = NoteForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return render(request, 'ajax_success.html',
                 {'form': NoteForm()})
            return HttpResponseRedirect(reverse('index'))
        if request.is_ajax():
            return render(request, 'ajax_fail.html', {'form': form})
        return render(request, 'add_note.html', {'form': form})
    form = NoteForm()
    return render(request, 'add_note.html', {'form': form})


def count(request):
    '''
    View to test that symbols count with NoteForm works
    with two forms at the same time.
    '''
    form1 = NoteForm()
    form2 = NoteForm()
    return render(request, 'count.html', {'forms': [form1, form2]})


def random_note(request):
    '''Returns random note'''
    note = Note.objects.order_by('?')[0]
    context = {'title': note.title, 'text': note.text, 'image': note.image}
    return render(request, 'show_note.html', context)


def test_embeddable_widget(request):
    '''Returns data to render with embeddable widget'''
    return render(request, 'emb_widg.html', {'site': request.get_host()})

def serve_embed_widget(request):
    '''Serves emb_widg.js'''
    return render(request, 'embed_widget.js', {'site': request.get_host()})
