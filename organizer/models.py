from datetime import timedelta
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms


# many-to-one relationship aka foreign keys: https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_one/
class Class(models.Model):
    class_name = models.CharField(max_length=10, default="", unique=True)  # assuming the string is 'CS3240'

    def __str__(self):
        return self.class_name


class Section(models.Model):
    section_id = models.CharField(max_length=10, unique=True)
    professor = models.CharField(max_length=200, default="")
    days = models.CharField(max_length=7, default="")  # ex. MWF
    start_time = models.TimeField()
    end_time = models.TimeField()
    course = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.professor.split(',')[0]} | {self.days} {self.start_time}-{self.end_time}"

    def professor_lname(self):
        return self.professor.split(',')[0]

# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # link to Django User mdoel
    schedule = models.ManyToManyField(Class)
    sections = models.ManyToManyField(Section)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class NotesGroup(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Class, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)


class Notes(models.Model):
    title = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='files/')
    group = models.ForeignKey(NotesGroup, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title}"


class NotesUploadForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('title', 'pdf',)


class Assignment(models.Model):
    class_name = models.CharField(max_length=100)
    assignment = models.CharField(max_length=200, default=" ")
    deadline = models.DateField()
    completed = models.BooleanField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def ColorDeadlines(self):
        from datetime import timedelta, date
        delta = self.deadline - date.today()
        if delta <= timedelta(days=1):
            return "red" 
        elif delta > timedelta(days=1) and delta <= timedelta(days=3):
            return "yellow"
        else:
            return "green"


    def __str__(self):
        return f"{self.assignment}"
