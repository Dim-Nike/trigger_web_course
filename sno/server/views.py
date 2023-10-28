from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import StudentRegistrationForm, StudentLoginForm
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
            'students': Student.objects.order_by('count_point'),
        }

        return render(req, 'server/index3.html', data)
    else:
        return redirect('login')


def show_item(req, pk):
    if req.user.is_authenticated:
        auth_student = Student.objects.get(user=req.user)

        data = {
            'courses': Course.objects.filter(id=pk),
            'auth_students': auth_student,
            'other_courses': Course.objects.exclude(id=pk),
        }

        if req.method == 'POST':
            new_course = Course.objects.get(id=pk)
            if new_course not in auth_student.courses.all():
                auth_student.courses.add(new_course)
                new_course.student_many.add(auth_student)
                auth_student.count_point += new_course.start_point
            else:
                print('Курс уже добавлен')


        return render(req, 'server/item2.html', data)
    else:
        return redirect('login')


def show_author(req):
    return render(req, 'server/author.html')


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


def show_create(req):
    return render(req, 'server/create.html')
