from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from uuid import UUID
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Username or password is incorrect')
            return redirect('login')  # Redirect to login page if authentication fails
        else:
            login(request, user)
            return redirect('home')

    return render(request, 'base/login.html')

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
    context = {'room': room}
    return render(request, 'base/room.html', context)

def create_room(request):
    form = RoomForm()  # Initialize the form

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')
    context = {'form': form}
    return render(request, 'base/form.html', context)

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

def delete_room(request, pk):
    room = Room.objects.get(id=UUID(pk))
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

def logoutUser(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the home page