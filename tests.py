
from django_webtest import WebTest
from notes.models import Note


class MyTests(WebTest):
    fixtures = ['starting.json']

    def test_of_model(self):
        note = Note(title='sometitle', text='sometext')
        note.save()
        all_notes = Note.objects.all()
        self.assertIn(note, all_notes)

    def test_of_note_output_at_index_page(self):
        note = Note(title='sometitle', text='sometext')
        note.save()
        index_page = self.app.get('/')
        self.assertTemplateUsed(index_page, template_name='index.html')
        assert note.title in index_page
        assert note.text in index_page

    def test_that_admin_works(self):
        login_page = self.app.get('/admin').follow()
        form = login_page.form
        form[u'username'] = 'nikita'
        form[u'password'] = 'n1k1ta'
        res = form.submit()
        res = res.follow()
        assert u'/note/add/' in res.body
        #I'm not really sure what particular link should I press
        #UPD: got it from 'print res.body'
        add_note = res.click(href='/admin/notes/note/add/')
        #I've had form field list with this:
        #print add_note.form.fields
        form = add_note.form
        form[u'title'] = u'new_test_title'
        form[u'text'] = u'new_test_text'
        res = form.submit(u'_save')
        index_page = self.app.get('/')
        assert 'new_test_title' in index_page
        assert 'new_test_text' in index_page
