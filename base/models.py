import uuid
from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    # id = models.CharField(max_length=10, primary_key=True)  # Using CharField for a custom ID
    # If you want to use UUID as primary key, uncomment the following line and comment the line above
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)  # Foreign key to Topic, can be null
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Foreign key to User, can be null
    participants = models.ManyToManyField(User, related_name='participants', blank=True)  # Many-to-many relationship with User
    updated = models.DateTimeField(auto_now=True) #this will update the timestamp whenever the model is saved
    created = models.DateTimeField(auto_now_add=True) #this will store the timestamp when it was first created

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User, deletes messages if user is deleted
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Foreign key to Room, deletes messages if room is deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) #this will update the timestamp whenever the model is saved
    created = models.DateTimeField(auto_now_add=True) #this will store the timestamp when it was first created

    def __str__(self):
        return self.body[:50]  # Return the first 50 characters of the message body
