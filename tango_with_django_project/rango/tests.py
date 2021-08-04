from django.test import TestCase
from rango.forms import UserForm

class RegistrationFormTest(TestCase):
    def test_registration_form_collects_all_details(self):
        # Ensure that the registration form collects and saves all the details a person enters
        userform = UserForm(username='testingusername', email='testing@email.com', password='testingpassword')
        userform.save()

        self.assertEqual((UserForm.username=='testingusername', UserForm.email=='testing@email.com', UserForm.password=='testingpassword'), True)


class CorrectRegistrationTest(TestCase):
    def test_registration_only_collects_correct_details(self):
        # Ensure that the registration form only collects details that are correct (e.g. age cannot be a string)
        userform = UserForm(username='234', email='notanemail', password='&&&&')
        userform.save()

        self.assertEqual((UserForm.username!='string', UserForm.email!='string', UserForm.password!='string'), True)
