from django.urls import path
from django.urls.resolvers import URLPattern
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'organizer'  # set app namespace
urlpatterns = [
    path('', views.HomeView.home, name='home'),  # ex: /organizer/ aka homepage
    # path('login/', views.LoginView.login, name='login'),  # ex: /organizer/login/ aka login page
    # path('register/', views.register_student, name='register'),
    path('register_check/', views.checkIfStudentRegistered, name='check_register'),
    path('students/<str:class_name>/', views.StudentView.studentView, name='students'),
    path('profile/', views.ProfileView.profileView, name='profile'),  # ex: /organizer/profile/ aka profile page
    path('search/', views.SearchView.searchView, name='search'), # /organizer/search/ for class search page
    path('class/<str:class_name>/', views.ClassView.classView, name='classview'),
    path('join/<str:class_name>/', views.JoinClassView, name='join'),
    path('leave/<str:class_name>/', views.LeaveClassView, name='leave'),
    path('assignments/', views.AssignView, name='assignments'),
    path('upload/<int:notes_group>/', views.NotesUploadView, name='upload'),
    path('addGroup/', views.AddNotesGroupView, name='addGroup'),
    path('deletenotes/<int:notes_id>/', views.DeleteNotesView, name='delete_notes'),
    path('check_assignment/<int:assign_id>/', views.CheckAssignView, name='check_assign'),
    path('deleteassignment/<int:assign_id>/', views.DeleteAssignView, name='delete_assign'),
    path('populate/<int:start>/', views.populate_database_view, name='populate'),
    path('newjoke/', views.newJoke, name='joke')


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
