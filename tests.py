from os import remove, getcwd

import Image
import hashlib
from selenium import webdriver

from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.test import LiveServerTestCase

from notes.forms import NoteForm
from notes.models import Note


class MyTests(WebTest):
    fixtures = ['start.json']
    csrf_checks = False

    def test_of_model(self):
        '''Create simple Note object'''
        note = Note.objects.create(title='sometitle', text='sometext')
        all_notes = Note.objects.all()
        self.assertIn(note, all_notes)

    def test_of_note_output_at_index_page(self):
        '''Test that note exist in the list of all notes @index'''
        note = Note.objects.create(title='sometitle', text='sometext')
        index_page = self.app.get(reverse('index'))
        self.assertTemplateUsed(index_page, template_name='index.html')
        assert note.title in index_page
        assert note.text in index_page

    def test_that_admin_works(self):
        '''Test that we can add Note with django admin'''
        res = self.app.get(reverse('admin:notes_note_add'))
        form = res.form
        form[u'username'] = 'admin'
        form[u'password'] = 'admin'
        res = form.submit().follow()
        form = res.form
        form[u'title'] = u'new_test_title'
        form[u'text'] = u'new_test_text'
        res = form.submit(u'_save')
        index_page = self.app.get(reverse('index'))
        #here's my test is note added to the db
        #if not - we'll have an error here
        Note.objects.get(title='new_test_title', text='new_test_text')
        assert 'new_test_title' in index_page
        assert 'new_test_text' in index_page

    def test_adding_new_note(self):
        '''Tests note adding with add_note view'''
        add_page = self.app.get(reverse('add_note'))
        form = add_page.form
        form[u'title'] = 'test'
        form[u'text'] = 'test'
        response = form.submit(u'Submit')
        assert u'Ensure this value has at least 10 characters' in response
        form = response.form
        form[u'title'] = 'test'
        form[u'text'] = 'test_test_test'
        form.submit()
        assert u'test_test_test' in self.app.get(reverse('index'))

    def test_custom_widget(self):
        '''
        Test that we got distinct ids if we have different forms
        Not needed anymore
        '''
        pass
        # page = self.app.get(reverse('count'))
        # assert 'id="test"' in page
        # assert 'id="test2"' in page

    def test_custom_widget_in_admin(self):
        '''Test that custom widget exists in admin. Not needed anymore'''
        pass
        # testing_note = Note(title='sometitle', text='sometext1111')
        # testing_note.save()
        # login_page = self.app.get(reverse('admin:index'))
        # form = login_page.form
        # form[u'username'] = 'admin'
        # form[u'password'] = 'admin'
        # res = form.submit()
        # res = res.follow()
        # notes = res.click('Notes', href='/admin/notes/note/')
        # edit_note = notes.click('sometitle')
        # #test if onclick with default values exist here
        # assert "somef(&#39;default_id&#39;,&#39;output_default_id&#39;)" in \
        # edit_note

    def test_notes_nmbr_in_context(self):
        '''Test that we have number of notes at most pages'''
        testing_note = Note.objects.create(title='sometitle1',
         text='sometext1111')
        page = self.app.get(reverse('index'))
        assert page.context['notes_number'] == 1
        testing_note = Note.objects.create(title='sometitle2',
         text='sometext1111')
        page = self.app.get(reverse('add_note'))
        assert page.context['notes_number'] == 2

    def test_ajax(self):
        '''Test that ajax post works'''
        #'csrf_checks = False ' in the beginning was included because
        #I don't feel like manually providing csrf here is a right way to go.
        ajax_header = {'X_REQUESTED_WITH': 'XMLHttpRequest'}
        title = ['test']
        text = ['test']
        post_args = {'title': title, 'text': text}
        ajax_resp = self.app.post(reverse('add_note'), post_args, ajax_header)
        assert u'Ensure this value has at least 10 characters' in ajax_resp
        title = ['test']
        text = ['test_test_test']
        post_args = {'title': title, 'text': text, 'form_name': ['add_note']}
        ajax_resp = self.app.post(reverse('add_note'), post_args, ajax_header)
        assert u'Your message was sent. You can add a new one now.' in \
        ajax_resp
        assert u'test_test_test' in self.app.get(reverse('index'))

    def test_image_upload(self):
        '''Test of image upload'''
        title = 'test'
        text = 'test_test_test'
        f = open('file.txt', 'w')
        f.write('bubububu\n')
        f.close()
        post_content = dict(title=title, text=text)
        upfile = [('image', 'file.txt')]
        add_page_resp = self.app.post(reverse('add_note'), post_content,
         upload_files=upfile)
        assert u'not an image or a corrupted image' in add_page_resp
        remove('file.txt')
        #create an image file and add it to upload field
        form = add_page_resp.form
        assert form['title'].value == 'test'
        assert form['text'].value == 'test_test_test'
        im = Image.new('RGB', (100, 50))
        im.save('someimage.png', format='PNG')
        upfile = [('image', 'someimage.png')]
        new_add_resp = self.app.post(reverse('add_note'), post_content,
         upload_files=upfile).follow()
        #got to overcome
        assert u'media/images/someimage' in new_add_resp
        #testing if image is in database and an image
        note = Note.objects.get(title='test', text='test_test_test')
        Image.open(note.image).save('someimage2.png', format='PNG')
        im1 = open('someimage.png', 'rb').read()
        im2 = open('someimage2.png', 'rb').read()
        assert hashlib.md5(im1).hexdigest() == hashlib.md5(im2).hexdigest()
        remove('media/images/someimage.png')
        remove('someimage.png')
        remove('someimage2.png')

    def test_ajax_image_upload(self):
        '''Test of ajax image upload'''
        #setup part
        ajax_header = {'X_REQUESTED_WITH': 'XMLHttpRequest'}
        title = ['test']
        text = ['test_test_test']
        #fail part
        f = open('file.txt', 'w')
        f.write('bubububu\n')
        f.close()
        upfile = [('image', 'file.txt')]
        post_args = {'title': title, 'text': text}
        ajax_resp = self.app.post(reverse('add_note'), post_args, ajax_header,
         upload_files=upfile)
        assert u'not an image or a corrupted image' in ajax_resp
        #good part
        im = Image.new('RGB', (100, 50))
        im.save('someimage.png', format='PNG')
        upfile = [('image', 'someimage.png')]
        post_args = {'title': title, 'text': text, 'form_name': ['add_note']}
        ajax_resp = self.app.post(reverse('add_note'), post_args, ajax_header,
         upload_files=upfile)
        assert u'Your message was sent. You can add a new one now.' in \
        ajax_resp
        assert u'test_test_test' in self.app.get(reverse('index'))
        remove('someimage.png')
        remove('file.txt')
        remove('media/images/someimage.png')

    def test_custom_template_tag(self):
        '''Test of show_note template tag'''
        note = Note.objects.create(title='title1', text='text2')
        string = '{% load show_note %}{% show_note ' + str(note.id) + '%}'
        t = Template(string)
        c = Context({})
        rendered = t.render(c)
        assert note.title in rendered
        assert note.text in rendered

    def test_adding_new_css_classes_to_NewTextarea(self):
        '''Test of adding stuff with django-widget-tweaks. E.g., css'''
        form = NoteForm()
        string = '{% load widget_tweaks %}{{form.text|add_class:"new_class"}}'
        t = Template(string)
        c = Context({'form': form})
        rendered = t.render(c)
        assert 'class="new_class countable"' in rendered

    def test_mime_type_of_generated_js(self):
        '''Test if template-generated js is js, not html/text'''
        response = self.app.get(reverse('serve_widg'))
        assert response.content_type == 'application/x-javascript'



class SeleniumTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        # pass
        self.browser.quit()

    def not_test_sel_ajax(self):
        '''Test ajax from client side'''
        add_page = self.browser.get(self.live_server_url + reverse('add_note'))
        #input of not valid data
        title_field = self.browser.find_element_by_name('title')
        title_field.send_keys('title')
        text_field = self.browser.find_element_by_name('text')
        text_field.send_keys('text')
        submit_button = self.browser.find_element_by_name('Submit')
        submit_button.click()
        body = self.browser.find_element_by_tag_name('body')
        assert 'Ensure this value has at least' in body.text
        #input of valid data
        title_field = self.browser.find_element_by_name('title')
        text_field = self.browser.find_element_by_name('text')
        title_field.send_keys('title')
        text_field.send_keys('text_text_text')
        submit_button.click()
        body = self.browser.find_element_by_tag_name('body')
        assert 'Your message was sent. You can add a new one now.' in body.text

    def not_test_sel_ajax_image_upload(self):
        '''Test ajax image upload from client side'''
        add_page = self.browser.get(self.live_server_url + reverse('add_note'))
        title_field = self.browser.find_element_by_name('title')
        text_field = self.browser.find_element_by_name('text')
        title_field.send_keys('title')
        text_field.send_keys('text_text_text')
        im = Image.new('RGB', (100, 50))
        im.save('simage.png', format='PNG')
        image_field = self.browser.find_element_by_name("image")
        image_field.send_keys(getcwd() + "/simage.png")
        submit_button = self.browser.find_element_by_name('Submit')
        submit_button.click()
        page = self.browser.get(self.live_server_url + '/')
        img = self.browser.find_element_by_tag_name('img')
        img_src = img.get_attribute('src')
        assert 'simage.png' in img_src
        remove('simage.png')
        remove('media/images/simage.png')

    def not_test_embeddable_widget(self):
        '''Test that widget embeds'''
        note = Note.objects.create(title='sometitle1', text='sometext1')
        rand_page = self.browser.get(self.live_server_url +
         reverse('random_note'))
        assert note.title in self.browser.page_source
        widg_page = self.browser.get(self.live_server_url +
         reverse('emb_widg'))
        self.browser.implicitly_wait(30)
        body = self.browser.find_element_by_tag_name('body').text
        assert note.title in body
        assert note.text in body


#     I wasn't able to find solid and simple solution to test javascript
#     with webtest. so I'm using selenium for this
#     UPD: actually, this stuff don't also :(
  #Probably, I should send Key_up to the form here, as javascript replies to it
    # def test_can_count_symbols(self):
    #     self.browser.get(self.live_server_url + '/count/')
    #     body = self.browser.find_element_by_tag_name('body')
    #     #first input
    #     textinput = self.browser.find_element_by_id('test')
    #     textinput.send_keys('admin111', Keys.RETURN)
    #     #second input on the same page
    #     textinput2 = self.browser.find_element_by_id('test2')
    #     textinput2.send_keys('admin1111', Keys.ARROW_DOWN)
    #     #sequentual assert for two inputs
    #     self.assertIn('8', body.text)
    #     self.assertIn('9', body.text)
    #     #simmultaneous assert
    #     assert '8' in body.text and '9' in body.text
