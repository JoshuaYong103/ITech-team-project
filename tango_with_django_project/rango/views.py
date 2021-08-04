from collections import namedtuple
from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, MovieLists, Page, UserProfile,MovieCol
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime
from django.core.paginator import PageNotAnInteger, Paginator,EmptyPage
import requests
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    context_dict['extra'] = 'From the model solution on GitHub'
    
    visitor_cookie_handler(request)

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # Spoiler: now you DO need a context dictionary!
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None
    
    # You cannot add a page to a Category that does not exist... DM
    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  # This could be better done; for the purposes of TwD, this is fine. DM.
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

# def register(request):
  #  registered = False

  #  if request.method == 'POST':
  #      user_form = UserForm(request.POST)
 #       profile_form = UserProfileForm(request.POST)
#
  #      if user_form.is_valid() and profile_form.is_valid():
  #          user = user_form.save()
   #         user.set_password(user.password)
  #          user.save()

  #          profile = profile_form.save(commit=False)
  #          profile.user = user

   #         if 'picture' in request.FILES:
   #             profile.picture = request.FILES['picture']
            
   #         profile.save()
  #          registered = True
  #      else:
   #         print(user_form.errors, profile_form.errors)
 #   else:
     #   user_form = UserForm()
     #   profile_form = UserProfileForm()
    
   # return render(request, 'rango/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

#def user_login(request):
   # if request.method == 'POST':
    #    username = request.POST.get('username')
     #   password = request.POST.get('password')

     #   user = authenticate(username=username, password=password)

    #    if user:
     #       if user.is_active:
     #           login(request, user)
     #           return redirect(reverse('rango:index'))
     #       else:
     #           return HttpResponse("Your Rango account is disabled.")
    #    else:
    #        print(f"Invalid login details: {username}, {password}")
     #       return HttpResponse("Invalid login details supplied.")
   # else:
    #    return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

#@login_required
#def user_logout(request):
#    logout(request)
 #   return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

@login_required
def show_movies(request):
    fileredpage =""
    if 'q' in request.GET:
        q=request.GET['q']
        fileredpage=MovieLists.objects.filter(title__icontains=q).order_by('-imdbrating')
        print(q)   
    else:
        fileredpage=MovieLists.objects.all().order_by('-imdbrating')
    print("hello")
   
    if(MovieLists.objects.count()==0):
        result = requests.get('https://imdb-api.com/en/API/IMDbList/k_6x2ikd97/ls004285275')
        myjson=result.json()
        

        MovieLists.objects.all().delete()
    
        for item in myjson['items']:
            MovieLists.objects.create(movieid=item['id'], 
            title=item['title'], fullTitle=item['fullTitle'], 
            yearreleased=item['year'], imgpath=item['image'],
            imdbrating=item['imDbRating'],description=item['description'])

            
        myresult = {"count": MovieLists.objects.count(), "page": MovieLists.objects.all().values()}
    
    else:
        myresult=fileredpage
       

        paginator=Paginator(myresult,10)
        page=request.GET.get('page')

        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page=paginator.page(paginator.num_pages) 
    
        myresult ={
        'count':paginator.count,
        'page': page
        } 

    return render(request, 'rango/movie_mini.html',  myresult )
  
  

@login_required
def movie_detail(request,movieid):
      print(request.user)
      movie=MovieLists.objects.get(movieid=movieid)
      movie.save()
      username = request.POST.get('username')  
      myresult ={
       'username': username,
       'movie': movie
     } 
      return render(request, 'rango/movie_detail.html',  myresult )

# @login_required
# def register_profile(request):
   # form = UserProfileForm()

  #  if request.method == 'POST':
   #     form = UserProfileForm(request.POST, request.FILES)

   #     if form.is_valid():
   #         user_profile = form.save(commit=False)
   #         user_profile.user = request.user
   #         user_profile.save()

  #          return redirect(reverse('rango:index'))
  #      else:
  #          print(form.errors)

  #  context_dict = {'form': form}
  #  return render(request, 'rango/profile_registration.html', context_dict)

class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserProfileForm()
        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture},
                                {'age': user_profile.age},
                                {'location': user_profile.location})
        
        return (user, user_profile, form)
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        
        return render(request, 'rango/profile.html', context_dict)
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'rango/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:profile',
                                    kwargs={'username': username}))
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'rango/profile.html', context_dict)

class ColMovie(View):
    @method_decorator(login_required)
    def post(self,request):
        if not request.user.is_authenticated:
            return render(request,'login.html')
        movie_id=request.POST.get("movie_id")
        print(movie_id)
        fav_movie=MovieCol(user=request.user,movie_id=movie_id)
        fav_movie.save()
        return HttpResponse("well done")

class MyWatchList(View):
    @login_required  
    def get(self,request):
        col_movies=MovieCol.objects.filter(user=request.user)
        try:
            page=request.GET.get('page',1)
        except PageNotAnInteger:
            page=1
        p=Paginator(col_movies,4,request=request)
        col_movies=p.page(page)
        return render(request,'watchlist.html',{"col_movies":col_movies})
    
        
    
