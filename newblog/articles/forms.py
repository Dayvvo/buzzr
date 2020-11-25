from django import forms
from newblog.accounts.forms import regex, regex2, check
from .models import Contact
from .models import Article, Comments


class AddArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'slug',
            'auth',
            'title',
            'body',
            'genre',
            'images',
        ]

        def clean_title(self):
            title = self.cleaned_data.get('title')
            if Article.objects.filter(title=title).exists():
                raise forms.ValidationError('This title has already been used.Enter a different title')
            return title


class Contactform(forms.ModelForm):
    Fullname = forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )

    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'msgfield'})
    )


    class Meta:
        model = Contact
        fields = [
            'Fullname',
            'email'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not check(email):
            raise forms.ValidationError('Please enter a valid email')
        for i in Contact.objects.all():
            if check(email) and i.email == email:
                raise forms.ValidationError('This email is already part of our mailing list')

        return email


class CommentForm(forms.ModelForm):
    full_name = forms.CharField(
           max_length=50,
           widget=forms.TextInput(attrs={'placeholder': 'Full name'})
    )
    comment = forms.CharField(
           max_length=500,
           widget=forms.Textarea(attrs={'placeholder': 'Type your comment'})
    )

    class Meta:
        model = Comments
        fields = ['full_name','comment']


