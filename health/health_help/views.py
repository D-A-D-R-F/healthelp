from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from spotipy import client
from .models import User , Tablet , Facts , Blogs , Excercise , Recipies , Doctor , Comments , Maps
import requests
import datetime
import time
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import random
from django.utils.crypto import get_random_string
import os

def index(request):
    api = "https://disease.sh/v3/covid-19/all"
    data = requests.get(api).json()
    cases = str(data['cases'])
    for i in range(len(cases)):
        if i > 8:
            formatted = cases
        else:
            formatted = cases[0] + cases[1] + cases[2] + "," + cases[3] + cases[4] + cases[5] + "," + cases[6] + cases[7] + cases[8]
    return render(request , "health_help/index.html" , {
        'data':formatted , 
   })
   
@login_required
def tablets(request):
    if request.method == 'POST':
        tab_name = request.POST['tab_name']
        time_taken = request.POST['time_taken']

        tabs = Tablet(username = request.user , tablet_name  = tab_name , time_taken = time_taken)
        tabs.save()

        return HttpResponseRedirect(reverse("tablets"))
    else:
        user_tablets = Tablet.objects.filter(username = request.user).all()
   
        return render(request , "health_help/tablets.html" , {
            'tabs': user_tablets
        })

@login_required
def view_tab(request , tablet):
    if request.method == 'POST':
        doseage = request.POST['doseage']
        reason = request.POST['for']
        doctor = request.POST['prescribed_by']

        if doseage == "":
            dose = "No doseage provided."
        else:
            dose = doseage
        
        if reason == "":
            to_cure = "No data provided."
        else:
            to_cure = reason

        if doctor == "":
            prescribed_by = "No data provided."
        else:
            prescribed_by = doctor

        get_data = Tablet.objects.filter(username = request.user , tablet_name = tablet).first()
        get_data.doseage = dose
        get_data.reason = to_cure
        get_data.doctor = prescribed_by
        get_data.save()

        return HttpResponseRedirect(reverse("view_tab" , kwargs={'tablet':tablet}))
    else:
        data = Tablet.objects.filter(username = request.user , tablet_name = tablet).all()
        for d in data:
            dose_rendered = d.doseage 
            cure = d.reason
            doc = d.doctor
            t = d.time_taken
        return render(request , "health_help/view-tab.html" , {
        'tablet':tablet , 
        'doseage':dose_rendered,
        'doctor':doc , 
        'reason':cure , 
        'time': t
    })

@login_required
def delete_tablet(request , tablet):
    if request.method == 'POST':
        deleted = Tablet.objects.filter(username = request.user , tablet_name = tablet)
        deleted.delete()
        return HttpResponseRedirect(reverse("tablets"))
    else:
        return HttpResponseRedirect(reverse("tablets"))

@login_required
def facts(request):
    no = random.randint(1 , 40)
    facts = Facts.objects.filter(id = no).first()
    return render(request , "health_help/facts.html" , {
        'facts':facts.fact
    })

@login_required
def excercise(request):
    excercises = Excercise.objects.all()
    recipies1 = Recipies.objects.all()[0:10]
    recipies2 = Recipies.objects.all()[10:20]
    recipies3 = Recipies.objects.all()[20:30]

    return render(request , "health_help/excercise.html" , {
        'excercises':excercises , 
        'recipies1':recipies1,
        'recipies2':recipies2,
        'recipies3':recipies3,

        })

@login_required
def blog(request):
    all_posts = Blogs.objects.all()
    return render(request , "health_help/blog.html" , {
        'blogs':all_posts
    })

@login_required
def add_blog(request):
    if request.method == 'POST':
        username = request.user.username
        content = request.POST['content']
        title = request.POST['title']
        image = request.POST['image']

        if image == "":
            img = "https://images.pexels.com/photos/4439425/pexels-photo-4439425.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
        else:
            img = image
        unique = get_random_string(length=12)

        add = Blogs(unique_id = unique , title = title , text = content , image = img , user_name = username)
        add.save()

        return HttpResponseRedirect(reverse("blog"))
    else:             
        return render(request , "health_help/add_blog.html")

@login_required
def view_blog(request , unique_id):
    blog_info = Blogs.objects.filter(unique_id = unique_id).first()
    if blog_info.image == "https://images.pexels.com/photos/4439425/pexels-photo-4439425.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940":
        message = "No image was provided."
    else:
        message = blog_info.image
    return render(request , "health_help/view_blog.html" , {
        'title':blog_info.title , 
        'username':blog_info.user_name ,
        'image':blog_info.image , 
        'text' : blog_info.text,
        'message':message

    })

@login_required
def doctor(request):
    if request.method == 'POST':
        doc_email = request.POST['doctor-email']
        user_code = Doctor.objects.filter(username = request.user.username).first()
        join_code = user_code.link
        html_message = render_to_string('health_help/email_template.html' , {'code': join_code , 'doctor_email':doc_email , 'patient':request.user.username})
        template = render_to_string('health_help/email_message.txt' , {'code': join_code , 'doctor_email':doc_email , 'patient':request.user.username})
        send_mail(subject=f"Invite to view medical info of {request.user.username} on Healthelp." ,
        message=template ,
        from_email=settings.EMAIL_HOST_USER ,
        recipient_list=[doc_email] , 
        fail_silently=False,
        html_message=html_message
    )
        return HttpResponseRedirect(reverse("view_doc", kwargs={'code': join_code}))
    else:
        tablets_taken = Tablet.objects.filter(username = request.user).all()
        read_code = Doctor.objects.filter(username = request.user.username).first()
        if read_code:
            url = read_code.link
        elif not read_code:
            code = get_random_string(length=15)
            link = "http://127.0.0.1:8000/doctor/" + code
            insert = Doctor(username = request.user.username , link = link)
            insert.save()
            url = link
        return render(request , "health_help/doctor.html" , {
            'tablets':tablets_taken , 
            'code': url
        })

def view_doc(request , join_code):
    if request.method == 'GET':
        map_api_key = os.environ.get("MAP_API")
        formatted_code = "http://127.0.0.1:8000/doctor/" + join_code
        read_code = Doctor.objects.filter(link = formatted_code).first()
        if read_code:
            user_name = Doctor.objects.filter(link = formatted_code).first()
            get_user_name = User.objects.filter(username = user_name.username).first()
            comments = Comments.objects.filter(username = user_name.username).all()
            tablets = Tablet.objects.filter(username = get_user_name).all()
            map_data = Maps.objects.filter(username = user_name.username).all()
            return render(request , "health_help/doc.html" , {
            'tablets':tablets ,
            'user_name':user_name.username , 
            'code_to_join':join_code,
            'comments': comments ,
            'map_data':map_data,
            'link': f"https://www.google.com/maps/embed/v1/search?key={map_api_key}&q="
            })
        else:
            return HttpResponseRedirect(reverse("doctor"))
    else:
        formatted_code = "http://127.0.0.1:8000/doctor/" + join_code
        user_name = Doctor.objects.filter(link = formatted_code).first()
        comment = request.POST['comment']
        comment_name = request.POST['comment-name']
        insertion = Comments(link = user_name , username = user_name.username , comments = comment , comment_name = comment_name)
        insertion.save()


        return HttpResponseRedirect(reverse("view_doc" , kwargs={'join_code':join_code}))

@login_required
def embed_map(request):
    if request.method == 'POST':
        map_query = request.POST['map_query']
        doc_name = request.POST['name_doc']
        if map_query.find(' ') != None:
            formatted_query = map_query.replace(' ' , '+')
        elif map_query.find('  ') != None:
            formatted_query = map_query.replace('  ' , '+')
        elif map_query.find(' ') == None:
            formatted_query = map_query
        
        save_map = Maps(username = request.user.username , map_query = formatted_query , doctor_name = doc_name)
        save_map.save()

        read_code = Doctor.objects.filter(username = request.user.username).first()
        replace_code = read_code.link.replace('http://127.0.0.1:8000/doctor/' , '')
        return HttpResponseRedirect(reverse("view_doc" , kwargs={'join_code': replace_code}))

    else:
        return HttpResponseRedirect(reverse("doctor"))

def about(request):
    if request.method == 'POST':
        contact_name = request.POST['name-contact']
        contact_email = request.POST['email-contact']
        contact_message = request.POST['message-contact']
        send_mail(subject="Message from health-help." ,
        message=f"{contact_name} with email {contact_email} said {contact_message}." ,
        from_email=settings.EMAIL_HOST_USER ,
        recipient_list=['davis.furtado07@gmail.com'] , 
        fail_silently=False
        )

        return HttpResponseRedirect(reverse('about'))
    else:     
        return render(request , "health_help/about.html")



def login_view(request):
    if request.method == "POST":
    
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "health_help/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "health_help/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "health_help/register.html", {
                "message": "Passwords must match."
            })
        elif len(username) < 6:
            return render(request, "health_help/register.html", {
                "message": "Username should be atleast 6 characters"
            })
        elif len(email) < 3:
            return render(request, "health_help/register.html", {
                "message": "Email is too short"
            })
        elif len(password) < 8:
            return render(request, "health_help/register.html", {
                "message": "Password too short!"
            })
        else:
            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "health_help/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "health_help/register.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
