from django import forms


class StudentRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'sign__input', 'placeholder': 'Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'sign__input', 'placeholder': 'Password'}))
    remember = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'remember', 'class': 'sign__input'}))

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class StudentLoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'sign__input', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'sign__input', 'placeholder': 'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class ChapterCheckForm(forms.Form):
    feedback = forms.CharField(label="Отзыв о главе", max_length=255, widget=forms.TextInput(attrs={'class': 'sign__input', 'placeholder': 'Отзыв о главе'}))
    remarks = forms.CharField(label="Замечания", max_length=255, widget=forms.TextInput(attrs={'class': 'sign__input', 'placeholder': 'Замечания'}))
    estimation = forms.ChoiceField(label="Оценка", choices=[
        (1, "Увлекательно"),
        (2, "Легко"),
        (3, "Сложно"),
        (4, "Не понятно"),
        (5, "Скучно")
    ],   widget=forms.Select(attrs={'class': 'sign__select'}))
    glossary = forms.CharField(label="Глоссарий", max_length=255, widget=forms.TextInput(attrs={'class': 'sign__input', 'placeholder': 'Глоссарий'}))
    chapter_pk = forms.IntegerField(label="id chapter")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estimation'].widget.attrs['placeholder'] = 'Оцени главу'

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class PresentationForm(forms.Form):
    type_choices = [
        ('sale', 'Put on sale'),
        ('instant', 'Instant sale price'),
        ('unlock', 'Unlock one purchased')
    ]

    file = forms.FileField(
        label='Загрузить презентацию',
        widget=forms.FileInput(attrs={'class': 'sign__file-upload', 'accept': 'video/mp4,video/x-m4v,video/*,.png,.jpg,.jpeg'})
    )
    linkGitHub = forms.CharField(
        label='Ссылка на GitHub',
        widget=forms.TextInput(attrs={'class': 'sign__input', 'placeholder': 'Репозиторий должен быть публичным'})
    )
    description = forms.CharField(
        label='Описание проекта',
        widget=forms.Textarea(attrs={'class': 'sign__textarea', 'placeholder': 'Не более 1000 символов'})
    )
    type = forms.ChoiceField(
        label='Type',
        choices=type_choices,
        widget=forms.RadioSelect(attrs={'name': 'type'})
    )
