from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.PROTECT)
    dsc = models.TextField(verbose_name='Описание о себе', blank=True, null=True)
    count_point = models.IntegerField(verbose_name='Количество баллов', default=0)
    projects = models.ManyToManyField('Project', verbose_name='Проекты', blank=True, null=True)
    courses = models.ManyToManyField('Course', verbose_name='Курсы', blank=True, null=True)


class Project(models.Model):
    pass


class CoursesCat(models.Model):
    class Meta:
        verbose_name = 'Категория курсов'
        verbose_name_plural = 'Категории курсов'

    name = models.CharField(verbose_name='Наименование категории', max_length=155)
    cat_id = models.CharField(verbose_name='id категории', max_length=155)

    def __str__(self):
        return self.name


class CoursesChapter(models.Model):
    class Meta:
        verbose_name = 'Глава курсов'
        verbose_name_plural = 'Главы курсов'

    name = models.CharField(verbose_name='Наименование главы', max_length=155)
    dsc = models.TextField(verbose_name='Описание')
    point = models.IntegerField(verbose_name='Баллы')

    def __str__(self):
        return self.name


class CoursesAuthor(models.Model):
    class Meta:
        verbose_name = 'Автор курсов'
        verbose_name_plural = 'Авторы курсов'

    name = models.CharField(verbose_name='Автор', max_length=155)

    def __str__(self):
        return self.name


class CoursesPrice(models.Model):
    class Meta:
        verbose_name = 'Цена курсов'
        verbose_name_plural = 'Цены курсов'

    is_price = models.BooleanField(verbose_name='Бесплатный/платный', default=False)
    price = models.IntegerField(verbose_name='Цена', default=0)

    def __str__(self):
        if self.is_price:
            return f'Платный: {self.price}р'
        else:
            return f'Бесплатный'


class Course(models.Model):
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    name = models.CharField(verbose_name='Название', max_length=155)
    dsc = models.TextField(verbose_name='Описание')
    img_preview_1 = models.ImageField(verbose_name='1 Фотография 260*300', upload_to='course/preview/1/%Y/%m/%d/')
    img_preview_2 = models.ImageField(verbose_name='2 Фотография 260*300', upload_to='course/preview/2/%Y/%m/%d/')
    img_preview_3 = models.ImageField(verbose_name='3 Фотография 260*300', upload_to='course/preview/3/%Y/%m/%d/')
    img_main = models.ImageField(verbose_name='Главная фотография', upload_to='course/img/%Y/%m/%d/')
    student_many = models.ManyToManyField(Student, verbose_name='Студенты')
    cat = models.ForeignKey(CoursesCat, verbose_name='Категория', on_delete=models.PROTECT)
    chapter = models.ManyToManyField(CoursesChapter, verbose_name='Главы')
    start_point = models.IntegerField(verbose_name='Start point')
    end_point = models.IntegerField(verbose_name='End point')
    author = models.ForeignKey(CoursesAuthor, verbose_name='Автор', on_delete=models.PROTECT)
    price = models.ForeignKey(CoursesPrice, verbose_name='Цена', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class CoursesChapterCheck:
    class Meta:
        verbose_name = 'Проверка глав курсов'
        verbose_name_plural = 'Проверки глав курсов'

    name_chapter = models.CharField(verbose_name='Наименование главы', max_length=155)
    is_passed = models.BooleanField(verbose_name='Пройдено')
    is_accepted = models.BooleanField(verbose_name='Принято')
    comment = models.TextField(verbose_name='Комментарий админа')
    comment_user = models.TextField(verbose_name='Комментарий пользователя')

class CoursesCheck(models.Model):
    class Meta:
        verbose_name = 'Проверка курсов'
        verbose_name_plural = 'Проверки курсов'

    student = models.ForeignKey(Student, verbose_name='Пользователь', on_delete=models.PROTECT)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.PROTECT)
    chapter_many = models.ManyToManyField(CoursesChapterCheck, verbose_name='Главы', null=True, blank=True)
    is_finish = models.BooleanField(verbose_name='Пройден')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)






