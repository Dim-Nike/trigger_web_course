from django.contrib import admin
from .models import *

admin.site.register(Student)
admin.site.register(CoursesCat)
admin.site.register(CoursesChapter)
admin.site.register(CoursesAuthor)
admin.site.register(CoursesPrice)
admin.site.register(Course)