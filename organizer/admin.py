from django.contrib import admin
from django.db.models.fields.related import ManyToManyField
from .models import Class, Section, Student, Assignment


class StudentAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field: ManyToManyField, request, **kwargs):
        if db_field.name=='schedule':
            kwargs['queryset']= Class.objects.all() #need to get it specified per student
        
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    fields=(('user'), 'schedule',)


admin.site.register(Class)
admin.site.register(Section)
admin.site.register(Student, StudentAdmin)
admin.site.register(Assignment)
