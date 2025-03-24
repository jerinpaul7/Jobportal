from audioop import error
from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime
from django.contrib import messages
import uuid
from jobportal.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import authenticate


# Create your views here.

def home(request):
    return render(request,'home.html')
def registerpage(request):
    if request.method == 'POST':
        f = userform(request.POST)
        if f.is_valid():
            u = f.cleaned_data['username']
            e = f.cleaned_data['email']
            ph = f.cleaned_data['ph']
            l = f.cleaned_data['location']
            d = f.cleaned_data['dob']
            hq = f.cleaned_data['hq']
            p = f.cleaned_data['password']
            cp = f.cleaned_data['confirmpassword']
            jobs = f.cleaned_data['jobs']

            if p == cp:
                d = usermode(username=u, email=e, ph=ph, location=l, dob=d, hq=hq, password=p, jobs=jobs)
                d.save()
                return redirect(u_login)

    return render(request, 'register.html')

def u_login(request):
    if request.method=='POST':
        x=usermode.objects.all()
        email = request.POST.get('email')
        p = request.POST.get('password')
        for i in x:
            if email == i.email and p==i.password:
                unm=i.username
                e=i.email
                ph=i.ph
                print(i.ph)
                hq=i.hq
                id1=i.id
                d={'unm':unm,'e':e,'ph':ph,'hq':hq,'id1':id1}
                return render(request,'userprofile.html',d)
        else:
            return HttpResponse("invalid credentails")
    return render(request, 'login.html')
def c_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'company not found')
            return redirect(c_login)
        profile_obj=companymodel.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified check your email')
            return redirect(c_login)
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'incorrect email or password')
            return redirect(c_login)
        obj=companymodel.objects.filter(user=user)
        return render(request,'companyindex.html',{'obj':obj})
    return render(request,'companylogin.html')
def c_register(request):
    if request.method=='POST':
        username=request.POST.get('usr')
        email=request.POST.get('email')
        password=request.POST.get('p')
        cpassword=request.POST.get('cp')
        if password==cpassword:
            if User.objects.filter(username=username).first():
                messages.success(request,'username already taken')
                return redirect(c_register)
            if User.objects.filter(email=email).first():
                messages.success(request,'email already exist')
                return redirect(c_register)
            user_obj=User(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token=str(uuid.uuid4())
            profile_obj=companymodel.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            send_mail_regis(email,auth_token)
            return HttpResponse("success")
        else:
            return HttpResponse("password doesnt match")


    return render(request,'companyregistartion.html')

def about(request):
    return render(request,'about.html')

def send_mail_regis(email,token):
    subject='account verified'
    message =f'click here to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)
def edituser(request,id1):
    x=usermode.objects.get(id=id1)
    return render(request,'updateuser.html',{'d':x})
def update(request, id):
    if request.method == 'POST':
        f = userform(request.POST)
        p = request.POST.get('password')
        cp = request.POST.get('confirmpassword')

        if p == cp:
            if f.is_valid():
                try:
                    x = usermode.objects.get(id=id)
                    x.username = request.POST.get('username')
                    x.email = request.POST.get('email')
                    x.ph = request.POST.get('ph')
                    x.location = request.POST.get('location')
                    x.jobs = request.POST.get('jobs')
                    x.hq = request.POST.get('hq')
                    x.password = request.POST.get('password')

                    # Convert `dob` properly
                    dob_str = request.POST.get('dob')
                    if dob_str:
                        x.dob = datetime.strptime(dob_str, '%Y-%m-%d')  # Convert to datetime

                    x.save()
                    return redirect(u_login)
                except Exception as e:
                    return HttpResponse(f"Error: {str(e)}")
            else:
                return HttpResponse(f"Invalid values: {f.errors}")  # Show form errors
        else:
            return HttpResponse("Passwords didn't match")
    else:
        return HttpResponse("Invalid request method")
def verify(request,auth_token):
    profile_obj=companymodel.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account is already verified')
            return redirect(c_login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'account has been verified')
        return redirect(c_login)
    else:
        return redirect(error)
def error(request):
    return render(request,'error.html')
def postfo(request,id):
    obj=companymodel.objects.get(id=id)
    if request.method=='POST':
        f=jobpost(request.POST)
        if f.is_valid():
            n=f.cleaned_data['companyname']
            e=f.cleaned_data['email']
            jn=f.cleaned_data['jobname']
            w=f.cleaned_data['work']
            ex=f.cleaned_data['experience']
            jt=f.cleaned_data['jobtype']
            m=jobpostmodel(companyname=n,email=e,jobname=jn,work=w,experience=ex,jobtype=jt)
            m.save()
            return HttpResponse("job posted succesfully")
    return render(request,'postform.html',{'obj':obj})

def userprofile(request, userid):
    user = usermode.objects.get(id=userid)  # ✅ Fetch user details
    return render(request, 'userprofile.html', {'user': user})  # ✅ Pass user data to template

def showjob(request, id1):
    d = usermode.objects.get(id=id1)

    print(f"User {d.username} is searching for jobs. Preferred jobs: {d.jobs}")

    m = jobpostmodel.objects.all()
    if not m.exists():
        print("No jobs found in database!")

    ids = []
    job_preferences = [j.strip().lower() for j in d.jobs.split(',')]  # Normalize user preferences

    for i in m:
        print(f"Checking job: {i.jobname}, Company: {i.companyname}")

        if i.jobname.strip().lower() in job_preferences:
            print(f"Match found: {i.jobname}")
            ids.append(i)

    print(f"Final job list for user {d.username}: {[job.jobname for job in ids]}")

    return render(request, 'showjobs.html', {'ids': ids, 'userid': id1})

def applypage(request,id,userid):
    d = usermode.objects.get(id=userid)
    m = jobpostmodel.objects.get(id=id)
    if request.method=='POST':
        f=aplliedjobs(request.POST,request.FILES)
        if f.is_valid():
            n=f.cleaned_data['name']
            e=f.cleaned_data['email']
            p=f.cleaned_data['ph']
            dob=f.cleaned_data['dob']
            hq=f.cleaned_data['hq']
            cname=f.cleaned_data['cname']
            jobname=f.cleaned_data['jobname']
            resume=f.cleaned_data['resume']
            sav=aplliedjobsmodel(name=n,email=e,ph=p,dob=dob,hq=hq,cname=cname,jobname=jobname,resume=resume,userid=userid)
            sav.save()
            messages.success(request, "Application submitted successfully!")

            return redirect(reverse('userprofile', args=[userid]))
        else:
            messages.error(request, "Please enter correct values.")
    return render(request,'applyform.html',{'d':d,'m':m})



def aplliedjobs1(request, id1):
    s = aplliedjobsmodel.objects.filter(userid=id1)  # ✅ Get applied jobs for the user
    return render(request, 'aplliedjobs.html', {'s': s})  # ✅ Render applied jobs template

def viewapplied(request,id):
    d=companymodel.objects.get(id=id)
    s=aplliedjobsmodel.objects.filter(cname=d.user.username)
    return render(request,'viewapplied.html',{'s':s})
def viewcompany(request):
    d=companymodel.objects.all()
    return render(request,'viewcompany.html',{'d':d})
def sendmail(request,id):
    d=companymodel.objects.get(id=id)
    if True:
        if request.method == 'POST':
            f = MailForm(request.POST)
            if f.is_valid():
                email = f.cleaned_data['email']
                subject = f.cleaned_data['subject']
                message = f.cleaned_data['message']
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[email],
                        fail_silently=False
                    )
                    return HttpResponse("mail sent successfully")
                except Exception as e:
                    return HttpResponse(f'failed to send mail:{str(e)}')
            else:
                return HttpResponse("enter crrct values")
        else:
            return render(request, 'send.html', {'d':d})



