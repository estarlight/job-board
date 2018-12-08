from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import *
import bcrypt
import re
# Create your views here.

def index(request):
    return render(request, 'handy_helper/index.html')

def register(request, methods='POST'):

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    request.session['error'] = False
    # request.session['action'] = request.POST['action']

    if len(request.POST['first_name']) < 1:
        messages.error(request, 'First name is required!')
        request.session['error'] = True
    elif not request.POST['first_name'].isalpha():
        messages.error(request, "First Name cannot contain numbers")
        request.session['error'] = True


    if len(request.POST['last_name']) < 1:
        messages.error(request, 'Last name is required!')
        request.session['error'] = True
    elif not request.POST['last_name'].isalpha():
        messages.error(request, "Last Name cannot contain numbers")
        request.session['error'] = True
    
    if len(request.POST['password']) < 8:
        messages.error(request, 'Password must be longer than 8 characters')
        request.session['error'] = True
    
    if not request.POST['password'] == request.POST['password_confirm']:
        messages.error(request, 'Passwords do not match')
        request.session['error'] = True

    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request, 'Please enter a valid email address')
        request.session['error'] = True
    
    if User.objects.filter(email = request.POST['email']).exists():
        messages.error(request, 'This email already exists. Please login.')
        request.session['error'] = True

    if request.session['error'] == True:
        return redirect('/')
    else:

        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        correct_hashed_pw = hashed_pw.decode('utf-8')

        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=correct_hashed_pw)

        new_user.save()

        request.session['user_id'] = new_user.id

        return redirect('/dashboard')


def login(request, methods='POST'):

    try:
        user = User.objects.get(email=request.POST['email'])
    except User.DoesNotExist:
        messages.error(request, 'Your email does not exists. Please register.')
        return redirect('/')


    result = bcrypt.checkpw(request.POST['password'].encode(),user.password.encode())

    if result:
        request.session['user_id'] = user.id
        
    else:
        messages.error(request, 'Email/Password does not match. Please try again.')

    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect ('/')

def dashboard(request):
    
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')

    context = {
        "jobs" : Job.objects.exclude(added_user_id__in=User.objects.all()),
        "my_jobs" : Job.objects.filter(added_user__id=request.session['user_id']),
        "logged_user" : User.objects.get(id=request.session['user_id'])

    }

    return render(request, 'handy_helper/dashboard.html', context)

def createjob(request):
    return render(request, 'handy_helper/createjob.html')


def create_process(request, methods="POST"):

    request.session['error'] = False

    if len(request.POST['title']) <1:
        messages.error(request,'Title is required')
        request.session['error'] = True
    elif len(request.POST['title']) <3:
        messages.error(request,'Title must be longer than 3 characters')
        request.session['error'] = True
    
    if len(request.POST['description']) <1:
        messages.error(request,'Description is required')
        request.session['error'] = True
    elif len(request.POST['description']) <10:
        messages.error(request,'Description must be longer than 10 characters')
        request.session['error'] = True
    
    if len(request.POST['location']) <1:
        messages.error(request,'Location is required')
        request.session['error'] = True

    if request.session['error'] == True:
        return redirect('/createjob')
    else:
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']

        created_user = User.objects.get(id=request.session['user_id'])

        Job.objects.create(title=title, description=description, location=location, created_user=created_user)

        return redirect ('/dashboard')

def view(request, id):

    context = {
        "job" : Job.objects.get(id=id)
    }

    return render(request, 'handy_helper/view.html', context)

def edit(request, id):

    context = {
        "job" : Job.objects.get(id=id)
    }

    return render(request, 'handy_helper/edit.html', context)

def edit_process(request, methods='POST'):

    id = request.POST['id']
    job = Job.objects.get(id=id)

    job.title = request.POST['title']
    job.description = request.POST['description']
    job.location = request.POST['location']
    job.save()

    return redirect('/dashboard')

def cancel(request, id):

    job = Job.objects.get(id=id)
    job.delete()
    return redirect('/dashboard')

def addjob(request, id):
    
    job = Job.objects.get(id=id)

    job.added_user = User.objects.get(id=request.session['user_id'])
    job.save()

    return redirect('/dashboard')

def done(request, id):

    job = Job.objects.get(id=id)
    
    user = User.objects.get(id=request.session['user_id'])

    job.added_user.remove(user)
    job.save()
    job.delete()

    return redirect('/dashboard')



