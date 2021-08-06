from django.test import TestCase
from rango.forms import UserForm
from django.test.client import Client
from django.contrib.auth.models import User
from django.db import models
from populate_script import populate
from django.urls import reverse
from rango.models import MovieLists
from rango import forms
def create_user_object():
    user = User.objects.get_or_create( 
        username='Tester',
    )[0]
    user.set_password('test123')
    user.save()

    return user
class RegistrationFormTest(TestCase):
    def test_registration_form_collects_all_details(self):
        # Ensure that the registration form collects and saves all the details a person enters
        userdata={'username':'testingusername', 'email':'testing@email.com', 'password':'testingpassword'}
        userform = forms.UserForm(data=userdata)
        userform.save()
        self.assertEqual(userform.is_valid(), True)
class test_log_in_page(TestCase):
    #movielist should only be displayed when user is logged in
    def test_logged_in(self):
        user_object=create_user_object()
        self.client.login(username='Tester',password='test123')
        content=self.client.get(reverse('rango:index')).content.decode()

        self.assertTrue('href="/rango/movielist/"' in content,True)
        self.assertTrue('href="/rango/watchlist/"' in content,True)
    def test_logged_out(self):
        content=self.client.get(reverse('rango:index')).content.decode()
    #when not logged in user should see login and register
        self.assertTrue('href="/accounts/login/"' in content,True)
        self.assertTrue('href="/accounts/register/"' in content,True)
class test_data_populate_in(TestCase):
    #movie got popped in the database
    def test_populate_script(self):
        populate()
        find_movies=MovieLists.objects.count()
        print(find_movies)
        self.assertTrue(find_movies==367,True)