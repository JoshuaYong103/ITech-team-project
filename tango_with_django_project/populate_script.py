import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import MovieLists,UserProfile,User,MovieCol,MovieLiked

# For an explanation of what is going on here, please refer to the TwD book.

def populate():  
    with open('data.json',encoding='utf8') as a:
      movieList = json.load(a)
    
    users=[
      ('test','abc123','20','Glasgow'),
    ]
   
    for movie in movieList['items']:
        add_movies(movie["id"],movie["title"], movie["fullTitle"],movie["year"],movie["image"],movie["imDbRating"],movie["description"])
    for i,j,k,m in users:
        add_user(i,j,k,m)
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
# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()