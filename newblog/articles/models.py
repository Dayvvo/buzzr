from django.db import models

from django.contrib.auth.models import User

PRIORITY = (
    ('Low', 'Low'),
    ('Mid', 'Medium'),
    ('High', 'High'),
)


class Comments(models.Model):
    full_name = models.CharField(max_length=100)
    comment = models.TextField(max_length=1000)
    time_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Contact(models.Model):
    Fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()


class Article(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)(
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    body = models.TextField()
    auth = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(blank=True)
    comments = models.ManyToManyField(Comments, null=True, blank=True)
    views = models.IntegerField(default=0)
    priority = models.CharField(default='Medium', max_length=20)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:90] + '...'



# Create your models here.
