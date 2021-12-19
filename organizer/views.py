from json.decoder import JSONDecodeError
from typing import Reversible
from django import template
from django.db.utils import IntegrityError
from django.http.response import HttpResponseRedirect
from django.views import generic
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse, request, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import FormView
from django.urls import reverse
from .models import Class, Section, Student, Notes, NotesUploadForm, NotesGroup, Assignment
from .forms import ProfileUpdateForm, RegisterForm, AssignForm, searchForm
from django.db import IntegrityError
import requests
import json
import re
import random
from datetime import timedelta, date

def AssignView(request):
    context={}
    if request.user.is_anonymous:
        registered = False

    else:
        registered = True
        if request.method == 'POST':
            form = AssignForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                student = request.user.student
                class_name = request.POST.get('class_name', '')
                assignment = data['assignment']
                deadline = data['deadline']
                assignment = Assignment(class_name=class_name, assignment=assignment, deadline=deadline, completed=False, student=student)
                assignment.save()
                return redirect('organizer:assignments')
        else:
            form = AssignForm()
            assignments = request.user.student.assignment_set.filter(completed=False).order_by('deadline')
            completed = request.user.student.assignment_set.filter(completed=True).order_by('deadline')
            context = {
                'assignform': form,
                'assignments': assignments,
                'completed': completed,
                'registered':registered,
            }
    return render(request, 'organizer/assignment.html', context)


class HomeView(generic.ListView):
    def home(request):
        template = loader.get_template('organizer/home.html')
        context={}
        
        if request.user.is_anonymous:
            registered = False

        else:
            registered = True
            sections = request.user.student.sections.all()
            days = {"M": [], "T": [], "W": [], "R": [], "F": []}
            for day in days:
                for section in sections:
                    if day in section.days:
                        days[day].append(section)
                days[day].sort(key=lambda s: s.start_time)

            context = {
                "classes": request.user.student.schedule.all(),
                "assignments": request.user.student.assignment_set.filter(completed=False, deadline__range=[date.today(),date.today()+timedelta(days=1)]).order_by('deadline'),
                "M": days["M"],
                "T": days["T"],
                "W": days["W"],
                "R": days["R"],
                "F": days["F"],
                "registered": registered,
            }
        return HttpResponse(template.render(context, request))


def newJoke(request):
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
        except JSONDecodeError:
            continue
        break
    return JsonResponse({"jokeSetup": setup, "jokeDelivery": delivery})


class ProfileView (generic.View):
    def profileView(request):
        template = 'organizer/profile.html'
        context={}
        if request.user.is_anonymous:
            registered = False

        else:
            registered = True
            if request.method == 'POST':
                form = ProfileUpdateForm(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    user = request.user
                    user.username = data['username']
                    user.first_name = data['first_name']
                    user.last_name = data['last_name']
                    user.save()
                return redirect('organizer:profile')
            else:
                user = request.user
                data = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name }
                form = ProfileUpdateForm(initial=data)
                context ={
                   'form': form,
                   'registered':registered, 
                }
        return render(request, template, context)


class ClassView (generic.View):
    def classView(request, class_name):
        template = loader.get_template('organizer/classview.html')
        course = Class.objects.get(class_name=class_name)
        notes_groups = course.notesgroup_set.all().order_by('-create_time')
        context = {
            'class': course,
            'notes_groups': notes_groups,
            'form': NotesUploadForm()
        }
        return HttpResponse(template.render(context, request))


class StudentView (generic.View):
    def studentView(request, class_name):
        template = loader.get_template('organizer/students.html')
        course = Class.objects.get(class_name=class_name)
        context = {
            'class': course,
            'students': course.student_set.all()
        }
        return HttpResponse(template.render(context, request))


class SearchView(generic.View):
    def searchView(request):
        template = loader.get_template('organizer/searchview.html')
        context={}
        if request.user.is_anonymous:
            registered = False

        else:
            registered = True
            classes = []
            if request.method == 'POST':
                form = searchForm(request.POST)
                if form.is_valid():
                    class_search = form.data['class_name'].upper()
                    class_search = class_search.replace(" ", "")
                    classes = Class.objects.filter(class_name__contains=class_search)
            else:
                form = searchForm()
                #classes = Class.objects.all()
                classes = request.user.student.schedule.all()
            context = {
                'classes': classes,
                'joined': request.user.student.schedule.all(),
                'form': form,
                'registered':registered,
            }
        return HttpResponse(template.render(context, request))


def JoinClassView(request, class_name):
    if request.method == 'POST':
        student = request.user.student
        course = Class.objects.get(class_name=class_name)
        student.schedule.add(course)
        section_id = request.POST.get('section', '')
        section = Section.objects.get(id=section_id)
        student.sections.add(section)
        student.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False})


def LeaveClassView(request, class_name):
    if request.method == 'POST':
        student = request.user.student
        course = Class.objects.get(class_name=class_name)
        sections = student.sections.filter(course=course)
        for section in sections:
            student.sections.remove(section)
            section.student_set.remove(student)
        student.schedule.remove(course)
        course.student_set.remove(student)
        return redirect('organizer:home')
    return redirect('organizer:home')


def checkIfStudentRegistered(request):
    try:
        verification=Student.objects.get(user=request.user)
        return redirect('organizer:home')
    except Student.DoesNotExist:
        user = request.user
        new_student = Student(user=user)
        new_student.save()
        return redirect('organizer:home') 


def NotesUploadView(request, notes_group):
    if request.method == 'POST':
        form = NotesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            title = data['title']
            pdf = data['pdf']
            group = NotesGroup.objects.get(id=notes_group)
            new_upload = Notes(title=title, pdf=pdf, group=group, student=request.user.student)
            new_upload.save()
    return redirect(request.META.get('HTTP_REFERER'))


def AddNotesGroupView(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name', '')
        title = request.POST.get('title', '')
        course = Class.objects.get(class_name=class_name)
        notesGroup = NotesGroup(title=title, course=course)
        notesGroup.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False})


def DeleteNotesView(request, notes_id):
    if request.method == 'POST':
        Notes.objects.get(id=notes_id).delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False})


def CheckAssignView(request, assign_id):
    if request.method == 'POST':
        assign = Assignment.objects.get(id=assign_id)
        completed = request.POST.get('completed', False)
        if completed == "true":
            assign.completed = True
        else:
            assign.completed = False
        assign.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False})

def DeleteAssignView(request, assign_id):
    if request.method == 'POST':
        Assignment.objects.get(id=assign_id).delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False})

def populate_database_view(request, start=0):
    data = requests.get('https://api.devhub.virginia.edu/v1/courses')
    #data = requests.get('http://stardock.cs.virginia.edu/louslist/Courses/')
    data.raise_for_status()

    if data.status_code != 204:
        dic = data.json()
        values = dic['class_schedules'].values()
        value_list = str(values)

        value_list = value_list[236:len(value_list)-3]
        result = re.findall(r'\[.*?\]', value_list)

        for ind in range(start, len(result)):
            class_values = result[ind]
            class_values = class_values[1:len(class_values)-1]
            class_values = class_values.replace("'", "")
            class_parameters = class_values.split(', ')

            if "2021 Fall" in class_parameters:
                # add class
                class_name = class_parameters[0]+class_parameters[1]
                class_exists = Class.objects.filter(class_name=class_name)
                if not class_exists:
                    Class.objects.create(class_name=class_name)

                # add section
                section_id = class_parameters[3]
                section_exists = Section.objects.filter(section_id=section_id)
                if not section_exists:
                    professor = class_parameters[-7]
                    days = class_parameters[-5]
                    start_time = class_parameters[-4]
                    end_time = class_parameters[-3]
                    course = Class.objects.get(class_name=class_name)
                    if professor and days and start_time and end_time:  # check all params exist
                        Section.objects.create(section_id=section_id, professor=professor, days=days, start_time=start_time, end_time=end_time, course=course)

    return JsonResponse({'ok': True})


