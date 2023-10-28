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