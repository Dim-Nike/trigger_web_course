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
    is_capitan = models.BooleanField(verbose_name='Капитан', default=False)

    def __str__(self):
        return self.user.username


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


class CoursesChapterCheck(models.Model):
    class Meta:
        verbose_name = 'Проверка глав курсов'
        verbose_name_plural = 'Проверки глав курсов'

    FEEDBACK_FIELDS = [
        ('1', 'Увллекательно'),
        ('2', 'Легко'),
        ('3', 'Сложно'),
        ('4', 'Не понятно'),
        ('5', 'Скучно'),
    ]

    name_chapter = models.CharField(verbose_name='Наименование главы', max_length=155)
    is_user_lecture = models.BooleanField(verbose_name='Пройдена лекция')
    is_user_practice = models.BooleanField(verbose_name='Пройдена практика')
    is_admin_practice = models.BooleanField(verbose_name='Принята практика')
    is_admin_lecture = models.BooleanField(verbose_name='Принята лекция')
    is_accepted = models.BooleanField(verbose_name='В процессе')
    comment = models.TextField(verbose_name='Комментарий админа', null=True, blank=True)
    comment_user = models.TextField(verbose_name='Отзыв о лекции', null=True, blank=True)
    feedback = models.CharField(verbose_name='Оценка главы', choices=FEEDBACK_FIELDS, max_length=1)
    note_user = models.CharField(verbose_name='Замечания', max_length=155, null=True, blank=True)
    glossary_user = models.CharField(verbose_name='Отзыв о практике', max_length=155, null=True, blank=True)
    data_start = models.DateTimeField(verbose_name='Дата начала', blank=True, null=True)
    data_end = models.DateTimeField(verbose_name='Дата окончания', blank=True, null=True)

    def __str__(self):
        return f'{self.name_chapter} - Стадия - {self.is_accepted}'


class CoursesCheck(models.Model):
    class Meta:
        verbose_name = 'Проверка курсов'
        verbose_name_plural = 'Проверки курсов'

    student = models.ForeignKey(Student, verbose_name='Пользователь', on_delete=models.PROTECT)
    chapter_many = models.ManyToManyField(CoursesChapterCheck, verbose_name='Главы курса', blank=True, null=True)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.PROTECT)
    is_finish = models.BooleanField(verbose_name='Пройден')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)


class Participants(models.Model):
    class Meta:
        verbose_name = 'Команда хакатона'
        verbose_name_plural = 'Команды хакатона'

    name = models.CharField(verbose_name='Название команды', max_length=155)
    team = models.ManyToManyField(Student, verbose_name='Участники')
    presentation = models.FileField(verbose_name='Презентация',
                                    upload_to='hackathon/participants/presentation/%Y/%m/%d/', null=True, blank=True)
    link_github = models.CharField(verbose_name='Ссылка на гитхаб', max_length=155, null=True, blank=True)
    dsc = models.TextField(verbose_name='Описание проекта', null=True, blank=True)
    type_project = models.CharField(verbose_name='Тип задания', max_length=155, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активно', default=True)
    place = models.IntegerField(verbose_name='Занятое место', default=0, blank=True, null=True)


class HackathonProjectsType(models.Model):
    class Meta:
        verbose_name = 'Тип задания в хакатоне'
        verbose_name_plural = 'Типы заданий в хакатоне'

    name = models.CharField(verbose_name='Название задания', max_length=155)
    dsc = models.TextField(verbose_name='Описание задания')
    is_active = models.BooleanField(verbose_name='Активно', default=True)


class CertificateConditions(models.Model):
    class Meta:
        verbose_name = 'Условие сертификата'
        verbose_name_plural = 'Условия сертификатов'

    first_place = models.IntegerField(verbose_name='Баллы за 1-ое место')
    is_use_active_1 = models.BooleanField(verbose_name='1 место')
    second_place = models.IntegerField(verbose_name='Баллы за 2-ое место')
    is_use_active_2 = models.BooleanField(verbose_name='2 место')
    third_place = models.IntegerField(verbose_name='Баллы за 3-е место')
    is_use_active_3 = models.BooleanField(verbose_name='3 место')
    is_active = models.BooleanField(verbose_name='Активно', default=True)


class Hackathon(models.Model):
    class Meta:
        verbose_name = 'Хакатон'
        verbose_name_plural = 'Хакатоны'

    name = models.CharField(verbose_name='Наименование', max_length=155)
    date_start = models.DateTimeField(verbose_name='Начало мероприятия')
    date_end = models.DateTimeField(verbose_name='Конец мероприятия')
    dsc = models.TextField(verbose_name='Описание')
    type_projects = models.ManyToManyField(HackathonProjectsType, verbose_name='Типы заданий')
    presentation = models.FileField(verbose_name='Презентация',
                                    upload_to='hackathon/presentation/%Y/%m/%d/', null=True, blank=True)
    photo = models.FileField(verbose_name='Фотография', upload_to='hackathon/photo/%Y/%m/%d/')
    team = models.ManyToManyField(Participants, verbose_name='Участвующие команды')
    prize = models.ManyToManyField(CertificateConditions, verbose_name='Условия призов')
    is_active = models.BooleanField(verbose_name='Активно', default=True)


class SettingsHackathon(models.Model):
    class Meta:
        verbose_name = 'Общие настройки хакатона'
        verbose_name_plural = 'Общие настройки хакатона'

    start = models.BooleanField(verbose_name='Начать хакатон')
    end = models.BooleanField(verbose_name='Завершить хакатон')






