import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import MovieLists,UserProfile,User,MovieCol,MovieLiked, Category, Page
from django.db import IntegrityError

# For an explanation of what is going on here, please refer to the TwD book.

def populate():  
    with open('data.json',encoding='utf8') as a:
      movieList = json.load(a)
    
    users=[
      ('test','abc123','20','Glasgow'),
    ]

    other_pages = [
        {'title':'Like Our Website',
        'url':"{% url 'rango:thank_you' %}"}
    ]

    cats = {'Review Us': {'pages': other_pages, 'likes': 0},}

    for cat, cat_data in cats.items():
        c = add_cat(cat, likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')
   
    for movie in movieList['items']:
        add_movies(movie["id"],movie["title"], movie["fullTitle"],movie["year"],movie["image"],movie["imDbRating"],movie["description"])
    for i,j,k,m in users:
        add_user(i,j,k,m)
    create_super_user('admin','admin@test.com','admin')
def add_movies(movieid, title, fullTitle,yearreleased,imgpath,imdbrating,description):
    c = MovieLists.objects.get_or_create(movieid=movieid)[0]
    c.movieid = movieid
    c.title = title
    c.fullTitle = fullTitle
    c.yearreleased = yearreleased
    c.imgpath = imgpath
    c.imdbrating = imdbrating
    c.description=description
    c.save()
    return c
def add_user(username,password,age,location):
    user=User.objects.get_or_create(username=username)[0]
    user.set_password(password)
    user.save()
    print(user.username)
    print(user,password)
    u=UserProfile.objects.get_or_create(user=user)[0]
    print(u.age)
    u.age=age
    u.location=location
    u.save()
    add_movie_to_likelist(user)
    add_movie_to_watchlist(user)
    return u
def add_movie_to_watchlist(user):
    fav_movie=MovieCol(user=user,movie_id="tt0029583")
    print(fav_movie)
    fav_movie.save()
def add_movie_to_likelist(user):
    Movie_Liked=MovieLiked(user=user,movie_id="tt0038718")
    Movie_Liked.save()
def create_super_user(username, email, password):
    '''
    for some reason get_or_create didn't work with creating the
    SuperUser so here is a try/except, with an IntegrityError
    raised if the SuperUser already exists
    '''
    try:
        u = User.objects.create_superuser(username, email, password)
        return u
    except IntegrityError:
        pass

def add_page(cat, title, url):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.save()
    return p
def add_cat(name, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.likes = likes
    c.save()
    return c
# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()