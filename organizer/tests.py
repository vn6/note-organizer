from django.conf.urls import url
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls.converters import register_converter
from organizer.models import Class, Student, Notes, NotesUploadForm, NotesGroup, Assignment
from organizer.forms import AssignForm, searchForm, RegisterForm, ProfileUpdateForm
from django.urls import reverse
import requests
import django.core.exceptions
from django.test.utils import setup_test_environment, teardown_test_environment
from json.decoder import JSONDecodeError
from django.test import RequestFactory
from django.db import models
from organizer.views import ProfileView, checkIfStudentRegistered, AssignView, HomeView, ClassView, StudentView, SearchView, JoinClassView, NotesUploadView, AddNotesGroupView, DeleteNotesView, CheckAssignView, populate_database_view


class NotesTest(TestCase):

    def test_class_object(self):
        cl = Class.objects.create(class_name="CS3240")
        self.assertTrue(isinstance(cl, Class))

    def test_notes_group_object(self):
        cl = Class.objects.create(class_name="CS3240")
        group = NotesGroup.objects.create(title="group_title", course=cl)
        self.assertTrue(isinstance(group, NotesGroup))

    def test_notes_object(self):
        cl = Class.objects.create(class_name="CS3240")
        group = NotesGroup.objects.create(title="group_title", course=cl)
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        n = Notes.objects.create(title="title", group=group, student=student)
        self.assertTrue(isinstance(n, Notes))

    def test_notes_object_data(self):
        cl = Class.objects.create(class_name="CS3240")
        group = NotesGroup.objects.create(title="group_title", course=cl)
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        n = Notes.objects.create(title="title", group=group, student=student)
        self.assertTrue(n.title=="title")

    def test_notes_group_update(self):
        cl = Class.objects.create(class_name="CS3240")
        group = NotesGroup.objects.create(title="group_title", course=cl)
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        n = Notes.objects.create(title="title", group=group, student=student)
        group.title = "new_title"
        self.assertTrue(isinstance(group, NotesGroup))

    def test_notes_update(self):
        cl = Class.objects.create(class_name="CS3240")
        group = NotesGroup.objects.create(title="group_title", course=cl)
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        n = Notes.objects.create(title="title", group=group, student=student)
        n.title = "new_title"
        self.assertTrue(isinstance(n, Notes))

class NotesFormTest(TestCase):

    def test_notes_form_invalid(self):
        data = {'title': 'test', 'pdf': '0xbadbadbad', }
        form = NotesUploadForm(data=data)
        self.assertFalse(form.is_valid())


class LoginTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_access_bad(self):
        response = self.client.get('/accounts/login/google/')
        self.assertEqual(response.status_code, 404)

    def test_login_access_good(self):
        data = requests.get('https://assignment-note-organizer-a-13.herokuapp.com/accounts/google/login/')
        data.raise_for_status()
        self.assertEqual(data.status_code, 200)


class SearchTests(TestCase):
    
    def setUp(self):
        self.client = Client()

    """
    No idea why this test isn't working. Says base.css is missing although it is included in organizer/static
   """
   #test if webpage is orking properly
    def test_class_page_exists(self):
        cl = Class.objects.create(class_name="ECE3751")
        response = self.client.get('/organizer/class/ECE3751/')
        self.assertEqual(response.status_code, 200)


    #test if a class that doesn't exist has a website
    def test_if_there_is_no_class(self):
        cl = Class.objects.create(class_name="ECE3753") #, professor="Sherrif")
        response = self.client.get('organizer/class/ECE3752/')
        self.assertEqual(response.status_code, 404)

    #test if the search form works 
    def test_search_form(self):
        data = {'class_name': 'ECE3240', }
        form = searchForm(data=data)
        self.assertTrue(form.is_valid())

    #testing if no data is inputed into the form
    def test_search_form_doesnt_work(self):
        data = {'class_name': 'ECE3240', }
        form = searchForm()
        self.assertFalse(form.is_valid())

    #testing with bad input
    def test_search_bad_input(self):
        data = {'class': 'ECE3240', 'temp_data': 'ECE3241'}
        form = searchForm(data=data)
        self.assertFalse(form.is_valid())

class ProfileFormTests(TestCase):

    def test_empty_profile_update_form(self):
        form = ProfileUpdateForm()
        self.assertFalse(form.is_valid())

    def test_profile_form(self):
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        data = {'username': 'johndoe', 'first_name': 'John', 'last_name':'Doe'}
        form = ProfileUpdateForm(data=data)
        self.assertTrue(form.is_valid())

class RegisterFormTests(TestCase):

    def test_empty_register_form(self):
        form = RegisterForm()
        self.assertFalse(form.is_valid())

    def test_register_form(self):
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        data = {'first_name': 'John', 'last_name':'Doe'}
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_register_update(self):
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        data = {'first_name': 'John', 'last_name':'Doe'}
        form = RegisterForm(data=data)
        student.user.first_name = form['first_name']
        student.user.last_name = form['last_name']
        self.assertTrue(isinstance(student, Student))


class AssignFormTests(TestCase):
    # test when no data is entered into the assignment form
    def test_empty_assign_form(self):
        form = AssignForm()
        self.assertFalse(form.is_valid())

    # test that assignment form works
    def test_assign_form(self):
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        data = {'class_name': 'CS3240', 'assignment': 'test', 'deadline': '11/14/2021'}
        form = AssignForm(data=data)
        self.assertTrue(form.is_valid())

    # test with invalid input
    def test_assign_invalid_input(self):
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        data = {'class_name': 'CS3240', 'assignment': 'test', 'deadline': 'bad input'}
        form = AssignForm(data=data)
        self.assertFalse(form.is_valid())

class AssignViewTests(TestCase):

    # test when there are no assignments 
    def test_no_assignments(self):
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        self.assertTrue(Assignment.DoesNotExist)

    # check that valid assignment successfully adds & saves
    def test_add_assignment(self):
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        a = Assignment.objects.create(class_name="CS3240", assignment="test", deadline="2021-11-14", completed="False", student=student)
        self.assertTrue(isinstance(a, Assignment))

    # test adding multiple assignments
    def test_multiple_assignments(self):
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        a = Assignment.objects.create(class_name="CS3240", assignment="test", deadline="2021-11-14", completed="False", student=student)
        b = Assignment.objects.create(class_name="CS3240", assignment="test2", deadline="2021-11-15", completed="False", student=student)
        c = Assignment.objects.create(class_name="CS3240", assignment="test3", deadline="2021-11-16", completed="False", student=student)
        self.assertTrue(isinstance(a, Assignment))
        self.assertTrue(isinstance(b, Assignment))
        self.assertTrue(isinstance(c, Assignment))

    def test_update_assignment(self):
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        a = Assignment.objects.create(class_name="CS3240", assignment="test", deadline="2021-11-14", completed="False", student=student)
        a.completed = "True"
        self.assertTrue(a.completed)

    def test_delete_assignment(self):
        user = User.objects.create(username="user1")
        student = Student.objects.create(user=user)
        a = Assignment.objects.create(class_name="CS3240", assignment="test", deadline="2021-11-14", completed="False", student=student)
        b = Assignment.objects.create(class_name="CS3240", assignment="test2", deadline="2021-11-15", completed="False", student=student)
        del a
        self.assertTrue(isinstance(b, Assignment))

class SIS_API_Test(TestCase):

    def test_connect_to_database(self):
        data = requests.get('https://api.devhub.virginia.edu/v1/courses')
        #data = requests.get('http://stardock.cs.virginia.edu/louslist/Courses/')
        data.raise_for_status()
        self.assertEqual(data.status_code,200)

class Quote_API_Test(TestCase):

    def test_connect_to_quote_server(self):
        data = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
        data.raise_for_status()
        self.assertEqual(data.status_code,200)

    def test_quote_parsing(self):
        quoteText=""
        quoteAuthor=""

        while True:
            try:
                response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
                quote = response.json()
                quoteText = quote['quoteText']
                quoteAuthor = quote['quoteAuthor']
            except JSONDecodeError: #for some reason this api returns lots of decode errors
                continue
            break
        self.assertTrue(len(quoteText)>0)
        # self.assertTrue(len(quoteAuthor)>0)  # may not have author

class Joke_API_Test(TestCase):

    def test_connect_to_joke_server(self):
        data = requests.get('https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,racist,sexist,explicit,religious,political')
        data.raise_for_status()
        self.assertEqual(data.status_code,200)

    def test_joke_parsing(self):
        setup = ""
        delivery = ""
        while True:
            try:
                response = requests.get('https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,racist,sexist,explicit,religious,political')
                joke = response.json()
                setup = joke['setup']
                delivery = joke['delivery']
            except KeyError:
                continue
            break
        self.assertTrue(len(setup)>0)
        self.assertTrue(len(delivery)>0)

class RFTests(TestCase):

    def test_register_no_student(self):
        rf = RequestFactory()
        request = rf.get('/organizer/register_check/')
        request.user = User.objects.create(username="test")
        response = checkIfStudentRegistered(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/organizer/')

    def test_register_with_student(self):
        rf = RequestFactory()
        request = rf.get('/organizer/register_check/')
        request.user = User.objects.create(username="test")
        request.student = Student.objects.create(user=request.user)
        response = checkIfStudentRegistered(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/organizer/')
    """
    def test_assign_view(self):
        rf= RequestFactory()
        request = rf.post('/organizer/assignments/')
        request.user = User.objects.create(username="test")
        request.student = Student.objects.create(user=request.user)
        a = Assignment.objects.create(class_name="CS3240", assignment="test", deadline="2021-11-14", completed="False", student=request.student)
        response = AssignView(request)
        print(response)
        self.assertEqual(2, 2)
    
    def test_home_view(self):
        rf= RequestFactory()
        request = rf.post('/organizer/assignments/')
        request.user = User.objects.create(username="test")
        request.student = Student.objects.create(user=request.user)
        a = Assignment.objects.create(class_name="CS3240", assignment="test", deadline="2021-11-14", completed="False", student=request.student)
        request.student.assignment_set.set([a])
        response = HomeView.home(request)
        print(response)
        self.assertEqual(2, 2)
    
    def test_profile_update_get(self):
        rf= RequestFactory()
        request = rf.get('/organizer/profile/')
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        response = ProfileUpdate(request, 'test@test.test')
        self.assertEqual(response.status_code, 200)

    def test_profile_update_post(self):
        rf= RequestFactory()
        payload = {'first_name': 'test', 'last_name': 'test'}
        request = rf.post('/organizer/profile/', data=payload)
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        response = ProfileUpdate(request, 'test@test.test')
        self.assertEqual(response.status_code, 200)
    
    def test_class_view(self):
        cl = Class.objects.create(class_name="CS3240")
        rf = RequestFactory()
        request = rf.get('/organizer/class/CS3240')
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        response = ClassView.classView(request, "CS3240")
        print(response)
        self.assertEqual(200, 200)
    
    def test_student_view(self):
        cl = Class.objects.create(class_name="CS3240")
        rf = RequestFactory()
        request = rf.get('/organizer/students/CS3240/')
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        response = StudentView.studentView(request, "CS3240")
        print(response)
        self.assertEqual(200, 200)

    def test_search_view(self):
        self.assertEqual(200, 200)

    def test_join_class_view_post(self):
        cl = Class.objects.create(class_name="CS3240")
        s = Section.objects.create(course=cl, id=1, start_time='09:00:00', end_time='10:15:00')
        rf= RequestFactory()
        payload = {'first_name': 'test', 'last_name': 'test', 'section': 1}
        request = rf.post('/organizer/profile/', data=payload)
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        response = JoinClassView(request, 'CS3240')
        print(response)
        self.assertEqual(response.status_code, 200)
    
    def test_notes_upload_view(self):
        rf= RequestFactory()
        cl = Class.objects.create(class_name="CS3240")
        group = NotesGroup.objects.create(title="group_title", course=cl)
        payload = {'title': 'test', 'pdf': 'test'}
        request = rf.post('/organizer/upload/1/', data=payload)
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        response = NotesUploadView(request, group)
        self.assertEqual(response.status_code, 200)
    """
    def test_add_notes_group_view_post(self):
        rf= RequestFactory()
        cl = Class.objects.create(class_name="CS3240")
        payload = {'class_name': 'CS3240', 'title': 'test'}
        request = rf.post('/organizer/addGroup/', data=payload)
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        response = AddNotesGroupView(request)
        self.assertEqual(response.status_code, 200)

    def test_add_notes_group_view_get(self):
        rf= RequestFactory()
        request = rf.get('/organizer/addGroup/')
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        response = AddNotesGroupView(request)
        self.assertEqual(response.status_code, 200)

    def test_delete_notes_view_get(self):
        rf= RequestFactory()
        request = rf.get('/organizer/deletenotes/1/')
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        response = DeleteNotesView(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_delete_notes_group_view_post(self):
        rf= RequestFactory()
        cl = Class.objects.create(class_name="CS3240")
        group = NotesGroup.objects.create(title="group_title", course=cl)
        payload = {'class_name': 'CS3240', 'title': 'test'}
        request = rf.post('/organizer/deletenotes/1/', data=payload)
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        n = Notes.objects.create(title="title", group=group, student=request.student, id=1)
        response = DeleteNotesView(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_check_assign_view_post_true(self):
        rf = RequestFactory()
        payload = {'completed': True}
        request = rf.post('/organizer/check_assignment/1/', data=payload)
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        a = Assignment.objects.create(class_name="CS3240", assignment="test", deadline="2021-11-14", completed="False",
                                      student=request.student, id=1)
        response = CheckAssignView(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_check_assign_view_post_false(self):
        rf = RequestFactory()
        payload = {'completed': False}
        request = rf.post('/organizer/check_assignment/1/', data=payload)
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        a = Assignment.objects.create(class_name="CS3240", assignment="test", deadline="2021-11-14", completed="False",
                                      student=request.student, id=1)
        response = CheckAssignView(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_check_assign_view_get(self):
        rf = RequestFactory()
        request = rf.get('/organizer/check_assignment/1/')
        request.user = User.objects.create(username="test", first_name="Test", last_name="Test")
        request.student = Student.objects.create(user=request.user)
        a = Assignment.objects.create(class_name="CS3240", assignment="test", deadline="2021-11-14", completed="False",
                                      student=request.student, id=1)
        response = CheckAssignView(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_populate_database_view(self):
        rf = RequestFactory()
        request = rf.get('/organizer/populate/')
        response = populate_database_view(request)
        self.assertEqual(response.status_code, 200)
