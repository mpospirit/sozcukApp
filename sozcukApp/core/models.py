from django.db import models
from datetime import datetime, timedelta

# Create your models here.
class Competitors(models.Model):
    name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    dateCreated = models.DateTimeField(default=datetime.now() + timedelta(hours=3), blank=True)

    class Meta:
        ordering = ['name']
        db_table = 'Competitors'

    def __str__(self):
        return self.name
    
class Words(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=10)
    definition = models.CharField(max_length=512)
    length = models.IntegerField(default=0)
    releaseDate = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.word
    
    class Meta:
        ordering = ['releaseDate']
        db_table = 'Words'

class Visitors(models.Model):
    ip = models.CharField(max_length=15)
    dateCreated = models.DateTimeField(default=datetime.now() + timedelta(hours=3), blank=True)
    agent = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return self.ip
    
    class Meta:
        ordering = ['dateCreated']
        db_table = 'Visitors'