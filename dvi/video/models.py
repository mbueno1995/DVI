from django.db import models
from datetime import datetime

# Create your models here.
class CUser(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=20)
    displayname=models.CharField(max_length=200)
    emailID=models.EmailField(max_length=300)

class Video(models.Model):
    category=models.CharField(max_length=300)
    videotitle=models.CharField(max_length=300)
    videodesc=models.CharField(max_length=500)
    videofile=models.FileField(upload_to='video/%Y/%m/%d', blank=True)
    thumbnailimg=models.ImageField(upload_to='video/%Y/%m/%d',blank=True)
    vusername = models.ForeignKey(CUser, related_name="video", on_delete=models.CASCADE, default=0, blank=True)
    created=models.DateTimeField(default=datetime.now)
    updated=models.DateTimeField(default=datetime.now)

    class Meta:
        ordering=['-created']

class Comment(models.Model):
    v_id=models.ForeignKey(Video, related_name="comment", on_delete=models.CASCADE, default=0, blank=True)
    cname=models.CharField(max_length=80)
    content=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.content)
