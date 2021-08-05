import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page,MovieCol,MovieLists

# For an explanation of what is going on here, please refer to the TwD book.

def populate():  
    with open('data.json',encoding='utf8') as a:
      movieList = json.load(a)
       
    # cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
    #         'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
    #         'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16} }
    
    
    #movieList = moviedetailLists.json()


      for movie in movieList['items']:
          add_movies(movie["id"],movie["title"], movie["fullTitle"],movie["year"],movie["image"],movie["imDbRating"],movie["description"])

      #  c =add_movies(movie["movieid"],movie["title"], mo vie["fullTitle"],movie["yearreleased"],movie["imgpath"],movie["imdbrating"],movie["description"] )
     
    
    # for c in Category.objects.all():
    #     for p in Page.objects.filter(category=c):
    #         print(f'- {c}: {p}')

# def add_page(cat, title, url, views=0):
#     p = Page.objects.get_or_create(category=cat, title=title)[0]
#     p.url=url
#     p.views=views
#     p.save()
#     return p

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

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()