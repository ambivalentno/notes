
from django_webtest import WebTest
from notes.models import Note

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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

    def test_adding_new_note(self):
        add_page = self.app.get('/add_note').follow()
        form = add_page.form
        form[u'title'] = 'test'
        form[u'text'] = 'test'
        response = form.submit(u'Submit')
        assert u'Ensure this value has at least 10 characters' in response
        form = response.form
        form[u'title'] = 'test'
        form[u'text'] = 'test_test_test'
        form.submit()
        # self.app.get('/').showbrowser()
        assert u'test_test_test' in self.app.get('/')

    def test_custom_widget(self):
        page = self.app.get('/count/')
        assert 'id="test"' in page
        assert 'id="test2"' in page

    def test_custom_widget_in_admin(self):
        testing_note = Note(title='sometitle', text='sometext1111')
        testing_note.save()
        login_page = self.app.get('/admin').follow()
        form = login_page.form
        form[u'username'] = 'nikita'
        form[u'password'] = 'n1k1ta'
        res = form.submit()
        res = res.follow()
        notes = res.click('Notes', href='/admin/notes/note/')
        edit_note = notes.click('sometitle')
        #test if onclick with default values exist here
        assert "somef(&#39;default_id&#39;,&#39;output_default_id&#39;)" in edit_note

    def test_notes_nmbr_in_context(self):
        testing_note = Note(title='sometitle1', text='sometext1111')
        testing_note.save()
        testing_note = Note(title='sometitle2', text='sometext1111')
        testing_note.save()
        page = self.app.get('/')
        assert 'notes number=2' in page
        page = self.app.get('/add_note/')
        assert 'notes number=2' in page

    def test_ajax(self):
        add_page = self.app.get('/add_note').follow()
        form = add_page.form
        form[u'title'] = 'test'
        form[u'text'] = 'test'
        form.submit(u'Submit')
        assert u'Ensure this value has at least 10 characters' in add_page
        form = response.form
        form[u'title'] = 'test'
        form[u'text'] = 'test_test_test'
        form.submit()
        assert u'Form submitted' in add_page
        assert u'test_test_test' in self.app.get('/')


# class SeleniumTests(LiveServerTestCase):
#     #I wasn't able to find solid and simple solution to test javascript
#     #with webtest. so I'm using selenium for this
#     #UPD: actually, this stuff don't also :(

#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.browser.implicitly_wait(3)

#     def tearDown(self):
#         self.browser.quit()

#     def test_can_count_symbols(self):
#         self.browser.get(self.live_server_url + '/count/')
#         body = self.browser.find_element_by_tag_name('body')
#         #first input
#         textinput = self.browser.find_element_by_id('test')
#         textinput.send_keys('admin111', Keys.RETURN)
#         #second input on the same page
#         textinput2 = self.browser.find_element_by_id('test2')
#         textinput2.send_keys('admin1111', Keys.ARROW_DOWN)
#         #sequentual assert for two inputs
#         self.assertIn('8', body.text)
#         self.assertIn('9', body.text)
#         #simmultaneous assert
#         assert '8' in body.text and '9' in body.text
