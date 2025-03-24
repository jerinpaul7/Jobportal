from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class usermode(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    ph = models.CharField(max_length=10)
    dob = models.DateTimeField()
    hq = models.CharField(max_length=20)
    jobs = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    confirmpassword = models.CharField(max_length=20)
class companymodel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
class jobpostmodel(models.Model):
    companyname=models.CharField(max_length=20)
    email=models.EmailField()
    jobname=models.CharField(max_length=30)
    work=models.CharField(max_length=20)
    experience=models.CharField(max_length=20)
    jobtype=models.CharField(max_length=20)
class aplliedjobsmodel(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    ph=models.CharField(max_length=10)
    dob=models.DateTimeField()
    hq=models.CharField(max_length=20)
    cname=models.CharField(max_length=20)
    jobname=models.CharField(max_length=20)
    resume=models.FileField()
    userid=models.CharField(max_length=10)

