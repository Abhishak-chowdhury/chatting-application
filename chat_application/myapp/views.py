from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import string, random
from myapp.models import *
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate,login as login_details,logout as logout_details
# Create your views here.

def SignUp(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        repassword=request.POST.get('repassword')
        if User.objects.filter(email=email).exists():
            messages.warning(request,'email already exists')
            return redirect('signup')
        if password !=repassword:
            messages.warning(request,'please check your re-entered password')
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            str_characters = string.ascii_lowercase + string.digits
            user = ''.join(random.choices(str_characters, k=5))
            full_user=username+'_'+user  
            user_obj=User(username=username+'_'+user,email=email)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request,f'successfully registered..{full_user}')
            return redirect('signup')
        else:
            user_obj=User(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request,f'successfully registered..{username}')
            return redirect('signup')
    return render(request,'signup.html')

def SignIn(request):
    if request.method == 'POST':
        password=request.POST.get('password')
        email=request.POST.get('email')
        try:
            u=User.objects.get(email=email)
            username=u.username
            if User.objects.filter(email=email).exists():
                user=authenticate(request,email = email ,password = password,username=username)
                if user is not None:
                    login_details(request,user)
                    messages.success(request,f'successfully login {username}')
                    return redirect('signin')
                else:
                    messages.warning(request,'login details are incorrect')
                    return redirect('signin')
            else:
                messages.warning(request,'email does not exists')
                return redirect('signin')
        except Exception as e:
            messages.warning(request,'email does not exists')
            return redirect('signin')
        
    return render(request,'signin.html')

def Logout(request):
    logout_details(request)
    messages.success(request,'thank you for spending some moment')
    return redirect('signup')
@login_required(login_url="signin")
def Join_Room(request):
    groups=ChatGroup.objects.all()
    contex={
        'groups':groups
    }
    return render(request,'join_room.html',contex)
@login_required(login_url="signin")
def Create_Room(request):
    if request.method == 'POST':
        group_name=request.POST.get('group')
        password=request.POST.get('password')
       
        if ChatGroup.objects.filter(name=group_name).exists():
            messages.warning(request,'Room name already exists')
            return redirect('createroom')
        else:
            hash_pass=make_password(password)
            chat_group_obj=ChatGroup(user=request.user,name=group_name,password=hash_pass)
            chat_group_obj.save()
            messages.success(request,f'Successfully created room {group_name}')
            return redirect('joinroom')
    return render(request,'create_room.html')
@login_required(login_url="signin")
def Room_validity(request):
    if request.method == 'POST':
        room_name=request.POST.get('room_name')
        password=request.POST.get('password')
        print(room_name,password)
        chat=ChatGroup.objects.get(name=room_name)
        if check_password(password,chat.password):
            return redirect('chat',room_name=room_name)
        else:
            messages.warning(request,'Your entered password is wrong')
            return redirect('joinroom')
        
@login_required(login_url="signin")    
def Chatting(request,room_name):
    chat_group_obj=ChatGroup.objects.get(name=room_name)
    chat_objs=Chat.objects.all()
    contex={
        'chat_group_obj':chat_group_obj,
        'chat_objs':chat_objs
    }
    return render(request,'chat.html',contex)