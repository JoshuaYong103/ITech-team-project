from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class MovieLists(models.Model):
    movieid=models.CharField(primary_key=True,max_length=15,unique=True)
    title=models.CharField(max_length=120,unique=False)
    fullTitle=models.CharField(max_length=250,unique=False)
    yearreleased=models.IntegerField(null=True)
    imgpath=models.CharField(max_length=400)
    imdbrating=models.FloatField(null=True)
    description=models.CharField(max_length=250,unique=False)

    class Meta:
      ordering = ['-movieid']


class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
#model for user profile
class UserProfile(models.Model):
    #each user has its own profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=10,null=False)
    location = models.CharField(max_length=150,null=False)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
#model for moviecollection
class MovieCol(models.Model):
    #a user can have many collected movies
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    #a movie can be collected by many collections
    movie=models.ForeignKey(MovieLists,on_delete=models.CASCADE)
        
    class Meta:
        verbose_name='Movie collection'
        verbose_name_plural=verbose_name
#model for movie get liked
class MovieLiked(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie=models.ForeignKey(MovieLists,on_delete=models.CASCADE)
    class Meta:
        verbose_name='Movie liked'
        verbose_name_plural=verbose_name