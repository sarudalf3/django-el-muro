from django.contrib import messages
from django.shortcuts import redirect, render
from WallApp.models import User, Message, Comment
import bcrypt

def index(request):
    print('*'*30)
    print('index route')
    context = {
    }
    if 'user' not in request.session: 
        #If user exists, send to wall
        messages.error(request, 'You are NOT logged')
        return render(request,'WallApp/login.html')
    
    return redirect('/wall') 
    #if user doesn't exist, send to login

def register(request):
    print('*'*30)
    print('Register')

    if request.method == "GET":
        return redirect('/')

    if request.method == "POST":
        print("Post register ",request.POST)
        
        errors = User.objects.reg_validation(request.POST)
        print(errors)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
        else:
            encrypted_pwd = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt()).decode()

            user = User.objects.create(
            first_name = request.POST['fname'],
            last_name = request.POST['lname'],
            email = request.POST['email'].lower(),
            password = encrypted_pwd
            )

            session_user = {
                'id': user.id,
                'name' : user.first_name + ' ' + user.last_name,
                'email' : user.email.lower()
            }
            
            print(session_user)
            request.session['user'] = session_user
            return redirect('/wall') 
            #Send to wall route

def login(request):
    print('*'*30)
    print('log in')
    if request.method == "GET":
        return redirect('/')

    if request.method == "POST":
        print("Post register ",request.POST)
        errors = User.objects.log_validation(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
        else:
            user = User.objects.get(email = request.POST['email'].lower())
            session_user = {
                'id' : user.id,
                'name' : user.first_name + ' ' + user.last_name,
                'email' : user.email.lower()
            }
            print(session_user)
            request.session['user'] = session_user
            return redirect('/wall')
            #Send to wall route

def destroy(request):
    print('*'*30)
    print('Clean session')
    del request.session['user']
    return redirect('/')

def wall(request):
    print('*'*30)
    print('The wall path')
    print(request.session['user'])
    #Access when there is a session opens
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'name': request.session['user']['name'],
        'messages_list' : Message.objects.all().order_by('-updated_at'),
        'comments' : Comment.objects.all().order_by('-updated_at'),
    }
    print(context)    
    return render(request,'WallApp/wall.html',context)
    #send all messages and contents of user for user

def message(request):
    if request.method == "POST":
        print("Message post ",request.POST)
        #save on database the comment in message
        new_message = Message.objects.create(
            message_text = request.POST['msg'],
            user = User.objects.get(id=request.session['user']['id'])
        )
    return redirect('/wall')

def post_comment(request, msg_id):
    print('*'*30)
    print('posting comment',msg_id)
    print("Comment Post ",request.POST)

    if request.method == "POST":
        new_comment = Comment.objects.create(
            comment_text = request.POST['comment'],
            user = User.objects.get(id=request.session['user']['id']),
            message = Message.objects.get(id=msg_id)
        )
    return redirect('/wall')

def destroy_message(request, msg_id):
    print('*'*30)
    print('delete message')
    comment_del = Message.objects.get(id=msg_id)
    comment_del.delete()
    return redirect('/wall')