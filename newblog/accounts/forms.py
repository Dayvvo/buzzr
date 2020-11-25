from django import forms
from django.contrib.auth import authenticate, get_user_model
import re
from django.contrib.auth.models import User
get_user = get_user_model()

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
regex2 ='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'


def check(email):

    return re.search(regex, email) or re.search(regex2, email)


class UserLoginForm(forms.Form):
    username_email = forms.CharField(
               max_length=100,
               widget=forms.TextInput(attrs={'placeholder': 'Username/Email'})
    )

    password = forms.CharField(
               max_length=100,
               widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username_email')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            check_email = User.objects.filter(email=username).exists()
            if not user and check_email == False:
                raise forms.ValidationError('Please enter a correct username/email and password.'
                                            'Note that both fields may be case sensitive')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'user_name', 'placeholder': 'Username'}))
    email = forms.EmailField(max_length=100,
                             required=False,
                             widget=forms.EmailInput(attrs={'id': 'user_email', 'required': 'False', 'placeholder': 'Email'})
                             )
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    password2 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password again'}))

    class Meta:
        model = get_user
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password == password2:
            ab = 2
        else:
            raise forms.ValidationError('Passwords must actually match')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        valid_user = User.objects.filter(username=username).exists()
        if valid_user:
            # for i in valid_user:
            #     if i.get_username() == username:
            raise forms.ValidationError('This username is already in use')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        valid_email = User.objects.filter(email=email).exists()
        if not check(email):
            raise forms.ValidationError('Please enter a valid email address')
        elif valid_email:
            raise forms.ValidationError('This email is already in use')
        return email

