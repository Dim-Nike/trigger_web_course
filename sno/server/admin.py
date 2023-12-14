from django.contrib import admin
from .models import *


class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'count_point']
    list_filter = ['courses']


class CoursesCatAdmin(admin.ModelAdmin):
    list_display = ['name', 'cat_id']


class CoursesChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'point']


class CoursesAuthorAdmin(admin.ModelAdmin):
    list_display = ['name']


class CoursesPriceAdmin(admin.ModelAdmin):
    list_display = ['price', 'is_price']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'cat', 'start_point', 'end_point', 'author', 'price']
    list_filter = ['cat', 'author', 'price']


class CoursesCheckAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'is_finish']
    list_filter = ['student', 'is_finish', 'course']


class CoursesChapterCheckAdmin(admin.ModelAdmin):
    list_display = ['name_chapter', 'is_user_lecture', 'is_user_practice',
                    'is_admin_practice', 'is_accepted']
    list_filter = ['name_chapter', 'is_user_lecture', 'is_user_practice',
                   'is_admin_practice',  'is_accepted']


class HackathonAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_start', 'date_end', 'is_active']
    list_filter = ['is_active']


class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ['name', 'type_project', 'is_active']
    list_filter = ['type_project', 'is_active']


class HackathonProjectsTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']


class CertificateConditionsAdmin(admin.ModelAdmin):
    list_display = ['first_place', 'is_use_active_1', 'second_place', 'is_use_active_2',
                    'third_place', 'is_use_active_3', 'is_active']

    list_filter = ['is_active']


admin.site.register(Student, StudentAdmin)
admin.site.register(CoursesCat, CoursesCatAdmin)
admin.site.register(CoursesChapter, CoursesChapterAdmin)
admin.site.register(CoursesAuthor, CoursesAuthorAdmin)
admin.site.register(CoursesPrice, CoursesPriceAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CoursesCheck, CoursesCheckAdmin)
admin.site.register(CoursesChapterCheck, CoursesChapterCheckAdmin)
admin.site.register(Hackathon, HackathonAdmin)
admin.site.register(Participants, ParticipantsAdmin)
admin.site.register(HackathonProjectsType, HackathonProjectsTypeAdmin)
admin.site.register(CertificateConditions, CertificateConditionsAdmin)

