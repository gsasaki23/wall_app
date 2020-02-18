from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime
from dateutil.relativedelta import relativedelta

# GET for Index page
def index(request):
    return render(request, 'index.html')    

# GET for Success page
def success(request):
    try:
        current_user = User.objects.get(id=request.session['user_id'])
        context = {
            "first_name":current_user.first_name,
            "current_id":current_user.id,
            "db_messages":Message.objects.all().order_by("-created_at"),
            "thirty_mins_ago":datetime.now()+relativedelta(minutes=-30)
        }
        return render(request, 'success.html', context)
    except KeyError:
        return redirect('/')

# POST for attempting to log in, if successful, route to success
def attempt_login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')    
    
    else:
        current_user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = current_user.id
        return redirect('/success')

# POST for attempting to register, if successful, register and route to success
def attempt_reg(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')    
    
    else:
        # Hashing PW
        pw_hash= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        # Creates new User
        User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            birthdate=request.POST["birthdate"],
            password=pw_hash,
        )
        current_user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = current_user.id
        
        return redirect('/success')

# POST for attempting to make a message, if successful, save and route to success
def attempt_message(request):
    errors = Message.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)    
    else:        
        # Creates new Message
        Message.objects.create(
            message =request.POST["message_text"], 
            message_user=User.objects.get(id=request.session['user_id'])
        )
    return redirect('/success')

# POST for deleting a message
def attempt_delete(request):
    message_to_del = Message.objects.get(id=request.POST['message_id'])
    message_to_del.delete()
    return redirect('/success')

# POST for creating a comment, then save and route to success
def attempt_comment(request):
    # Creates new comment
    Comment.objects.create(
        comment =request.POST["comment_text"], 
        parent_message = Message.objects.get(id = request.POST['message_id']),
        comment_user=User.objects.get(id=request.session['user_id'])
    )
    return redirect('/success')

# POST for logging out, clearing session
def logout(request):
    del request.session['user_id']
    return redirect('/')