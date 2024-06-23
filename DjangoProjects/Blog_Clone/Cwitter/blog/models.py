from django.db.models import Q
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea

# Create your models here.

class PostQuery(models.QuerySet):
    def search(self,query=None):
        qs = self
        if query is not None:
            or_lookup = ( Q(title__icontains=query) |
                          Q(text__icontains=query) |
                          Q(posted_by__username__icontains=query)
                          )
            qs = qs.filter(or_lookup).distinct()
        return qs

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuery(self.model,using = self._db)

    def search(self,query=None):
        return self.get_queryset().search(query=query)


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=200,null=True)
    profile_pic = models.ImageField(upload_to='profile_pics',default='No Image',choices=[('IMAGES/profile_pics/no_profile_pic.jpg', 'No Image'),
    ('IMAGES/profile_pics/avatar_1.jpg', 'Avatar 1'),
    ('IMAGES/profile_pics/avatar_2.jpg', 'Avatar 2'),
    ('IMAGES/profile_pics/avatar_3.jpg', 'Avatar 3'),
    ('IMAGES/profile_pics/avatar_4.jpg', 'Avatar 4'),
    ('IMAGES/profile_pics/avatar_5.jpg', 'Avatar 5'),
    ('IMAGES/profile_pics/avatar_6.jpg', 'Avatar 6'),
    ('IMAGES/profile_pics/avatar_7.jpg', 'Avatar 7'),
    ('IMAGES/profile_pics/avatar_8.jpg', 'Avatar 8'),
    ('IMAGES/profile_pics/avatar_9.jpg', 'Avatar 9'),
    ('IMAGES/profile_pics/avatar_10.jpg', 'Avatar 10')])
    context_object_name = 'user_profile'

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse("profile", kwargs={'pk':self.pk})

class Post(models.Model):
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.localtime)
    published_date = models.DateTimeField(blank=True,null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    objects = PostManager()

    def publish(self):
        self.published_date = timezone.localtime()
        self.save()

    def approved_comment(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk':self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    posted_by = models.CharField(max_length=50)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.localtime)
    approved_comment = models.BooleanField(default=True)

    def disapprove(self):
        self.approved_comment=False
        self.save()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("home")
