from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, Message
from uuid import UUID
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Username or password is incorrect')
            return redirect('login')  # Redirect to login page if authentication fails
        else:   
            login(request, user)
            link = request.GET.get('next') or request.POST.get('next')
            return redirect(link if link else 'home')  # Redirect to the prev URL or home page

    context = {'page': 'login'}
    return render(request, 'base/login.html', context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = UserCreationForm()  # Initialize the user creation form

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            link = request.GET.get('next') or request.POST.get('next')
            return redirect(link if link else 'home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'form': form}
    return render(request, 'base/login.html', context)
    


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |  # Filter rooms by topic name
        Q(description__icontains=q) |  # Filter rooms by description
        Q(name__icontains=q) | # Filter rooms by name
        Q(host__username__icontains=q)  # Filter rooms by host username
        )  # Fetch all rooms from the database
    
    room_count = rooms.count()  # Count the number of rooms
    topics = Topic.objects.all()  # Fetch all topics from the database
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'showSearchBar': True}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=UUID(pk))  # Fetch the room by its UUID
    roomMessages = room.message_set.all().order_by('-created')  # Fetch all messages related to the room
    participants = room.participants.all()  # Fetch all participants in the room
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('message')
        )
        room.participants.add(request.user)  # Add the user to the participants of the room
        message.save()
        return redirect('room', pk=room.id)

    context = {'room': room, 'roomMessages': roomMessages, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()  # Initialize the form

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')
    context = {'form': form}
    return render(request, 'base/form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=UUID(pk))  # Fetch the room by its UUID
    form = RoomForm(instance=room)  # Initialize the form with the room instance
    if(request.method == 'POST'):
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=UUID(pk))
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=UUID(pk))
    if request.method == 'POST':
        roomId = message.room.id
        message.delete()
        return redirect('room', pk=roomId)
    return render(request, 'base/delete.html', {'obj': message})

def logoutUser(request):
    logout(request)  # Log out the user
    link = request.GET.get('next') or request.POST.get('next')
    return redirect(link if link else 'home')