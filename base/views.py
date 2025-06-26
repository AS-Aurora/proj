from django.shortcuts import render, redirect
from .models import Room
from uuid import UUID
from .forms import RoomForm

def home(request):
    rooms = Room.objects.all()  # Fetch all rooms from the database
    context = {'rooms': rooms}
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