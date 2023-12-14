from datetime import datetime

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import StudentRegistrationForm, StudentLoginForm, ChapterCheckForm, PresentationForm
from .models import *


def show_index(req):
    return render(req, 'server/index.html')


def show_home(req):
    if req.user.is_authenticated:
        auth_student = Student.objects.get(user=req.user)
        data = {
            'courses_all': Course.objects.all(),
            'courses_1': Course.objects.filter(cat__cat_id='tab-1'),
            'courses_2': Course.objects.filter(cat__cat_id='tab-2'),
            'courses_3': Course.objects.filter(cat__cat_id='tab-3'),
            'courses_4': Course.objects.filter(cat__cat_id='tab-4'),
            'cat_courses': CoursesCat.objects.all(),
            'auth_students': auth_student,
            'students': Student.objects.order_by('-count_point'),
        }

        return render(req, 'server/index3.html', data)
    else:
        return redirect('login')


def show_item(req, pk):
    if req.user.is_authenticated:

        auth_student = Student.objects.get(user=req.user)



        if req.method == 'POST':
            new_course = Course.objects.get(id=pk)
            if new_course not in auth_student.courses.all():
                auth_student.courses.add(new_course)
                new_course.student_many.add(auth_student)
                new_course.save()
                auth_student.count_point += new_course.start_point
                auth_student.save()

                for course in Course.objects.filter(id=pk):
                    new_courses_check = CoursesCheck.objects.create(
                        student=Student.objects.get(user=req.user),
                        course=course,
                        is_finish=False
                    )
                    for i, chapter in enumerate(course.chapter.all()):
                        if i == 0:
                            new_chapter_check = CoursesChapterCheck.objects.create(
                                name_chapter=chapter,
                                is_user_lecture=False,
                                is_user_practice=False,
                                is_admin_practice=False,
                                is_admin_lecture=False,
                                is_accepted=True,
                                data_start=datetime.now(),
                                data_end=datetime.now()
                            )
                            new_courses_check.chapter_many.add(new_chapter_check)
                        else:
                            new_chapter_check = CoursesChapterCheck.objects.create(
                                name_chapter=chapter,

                                is_user_lecture=False,
                                is_user_practice=False,
                                is_admin_practice=False,
                                is_admin_lecture=False,
                                is_accepted=False,
                                data_start=datetime.now(),
                                data_end=datetime.now()
                            )
                            new_courses_check.chapter_many.add(new_chapter_check)

            else:
                auth_student.courses.remove(new_course)
                new_course.student_many.remove(auth_student)
                new_course.save()
                auth_student.count_point -= new_course.start_point
                auth_student.save()

        if Course.objects.get(id=pk) not in auth_student.courses.all():
            show_text_btn = True
        else:
            show_text_btn = False

        data = {
            'courses': Course.objects.filter(id=pk),
            'auth_students': auth_student,
            'other_courses': Course.objects.exclude(id=pk),
            'show_text_btn': show_text_btn
        }

        return render(req, 'server/item2.html', data)
    else:
        return redirect('login')


def show_author(req):
    if req.user.is_authenticated:
        auth_student = Student.objects.get(user=req.user)
        courses = auth_student.courses.all()
        check_courses = CoursesCheck.objects.filter(student=auth_student)
        form = ChapterCheckForm()
        hackathons = Hackathon.objects.filter(is_active=True)
        data = {
            'courses': courses,
            'auth_students': auth_student,
            'check_courses': check_courses,
            'form': form,
            'btn_send_check': ['Отправить лекции', 'Отправить практики', 'В ожидании', 'Следующая глава'],
            'hackathons': hackathons,
        }

        if req.method == 'POST':

            if req.POST.get('action') == 'stage_1':
                form = ChapterCheckForm(req.POST)
                feedback = form['feedback'].value()
                remarks = form['remarks'].value()
                estimation = form['estimation'].value()
                glossary = form['glossary'].value()
                chapter_pk = req.POST['chapter_pk']

                check_chapter_courses = CoursesChapterCheck.objects.get(id=chapter_pk)
                check_chapter_courses.feedback = estimation
                check_chapter_courses.comment_user = feedback
                check_chapter_courses.note_user = remarks
                check_chapter_courses.is_user_lecture = True
                check_chapter_courses.save()

            if req.POST.get('action') == 'stage_2':
                form = ChapterCheckForm(req.POST)
                feedback = form['feedback'].value()
                remarks = form['remarks'].value()
                estimation = form['estimation'].value()
                glossary = form['glossary'].value()
                chapter_pk = req.POST['chapter_pk']

                check_chapter_courses = CoursesChapterCheck.objects.get(id=chapter_pk)
                check_chapter_courses.glossary_user = feedback
                check_chapter_courses.is_user_practice = True
                check_chapter_courses.save()

            if req.POST.get('action') == 'finish':
                form = ChapterCheckForm(req.POST)
                chapter_pk = req.POST['chapter_pk']
                courses_pk = req.POST['courses_pk']
                check_courses = CoursesCheck.objects.get(id=courses_pk)
                check_chapter_courses = CoursesChapterCheck.objects.get(id=chapter_pk)
                check_chapter_courses.is_accepted = False
                check_chapter_courses.data_end = datetime.now()
                check_chapter_courses.save()

                auth_student = Student.objects.get(user=req.user)
                point = CoursesChapter.objects.get(name=check_chapter_courses.name_chapter).point
                auth_student.count_point += point
                auth_student.save()

                for el in check_courses.chapter_many.all():
                    if el.is_admin_practice and el.is_admin_lecture and not el.is_accepted:
                        continue
                    else:
                        el.data_start = datetime.now()
                        el.is_accepted = True
                        el.save()
                        print(el.name_chapter)
                        break

        return render(req, 'server/author.html', data)
    else:
        return redirect('login')


def show_register(req):
    if req.method == 'POST':
        form = StudentRegistrationForm(req.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['name'], password=form.cleaned_data['password'])
            student = Student.objects.create(user=user)
            return redirect('login')  # Перенаправление на страницу успешной регистрации
    else:
        form = StudentRegistrationForm()

    data = {
        'form': form
    }
    return render(req, 'server/signup.html', data)


def show_login(req):
    if req.method == 'POST':
        form = StudentLoginForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = StudentLoginForm()

    data = {
        'form': form
    }
    return render(req, 'server/signin.html', data)


def show_collection(req):
    return render(req, 'server/collection.html')


def show_create(req, pk):
    if req.user.is_authenticated:
        hackathon = Hackathon.objects.filter(id=pk)
        auth_student = Student.objects.get(user=req.user)
        team_hackathon = Participants.objects.filter(team=Student.objects.get(user=req.user), is_active=True)
        form = PresentationForm(req.POST)
        data = {
            'form': form,
            'auth_students': auth_student,
            'hackathon': hackathon,
            'auth_student': auth_student,
            'teams': team_hackathon

        }
        if req.method == 'POST':
            file = form.cleaned_data['file']
            linkGitHub = form.cleaned_data['linkGitHub']
            description = form.cleaned_data['description']

            print('File:', file)
            print('Link to GitHub:', linkGitHub)
            print('Description:', description)
            print('Type:', type)
        return render(req, 'server/create.html', data)

    else:
        return redirect('login')


def show_hackathon(req, pk):
    if req.user.is_authenticated:
        hackathon = Hackathon.objects.filter(id=pk)
        auth_student = Student.objects.get(user=req.user)
        team_hackathon = Participants.objects.filter(team=Student.objects.get(user=req.user), is_active=True)
        data = {
            'auth_students': auth_student,
            'hackathon': hackathon,
            'auth_student': auth_student,

        }

        return render(req, 'server/article.html', data)
    else:
        return redirect('login')


def show_prize(req):
    return render(req, 'server/404.html')
