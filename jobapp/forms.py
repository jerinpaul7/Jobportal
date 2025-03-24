from django import forms
class userform(forms.Form):
    username=forms.CharField(max_length=20)
    email=forms.EmailField()
    ph=forms.CharField(max_length=10,min_length=10)
    dob=forms.DateTimeField()
    hq=forms.CharField(max_length=20)
    jobs=forms.CharField(max_length=20)
    location=forms.CharField(max_length=20)
    password=forms.CharField(max_length=20)
    confirmpassword=forms.CharField(max_length=20)
class jobpost(forms.Form):
    companyname=forms.CharField(max_length=20)
    email=forms.EmailField()
    jobname=forms.CharField(max_length=30)
    work=forms.CharField(max_length=20)
    experience=forms.CharField(max_length=20)
    jobtype=forms.CharField(max_length=20)
class aplliedjobs(forms.Form):
    name=forms.CharField(max_length=20)
    email=forms.EmailField()
    ph=forms.CharField(max_length=10,min_length=10)
    dob=forms.DateTimeField()
    hq=forms.CharField(max_length=20)
    cname=forms.CharField(max_length=20)
    jobname=forms.CharField(max_length=20)
    resume=forms.FileField()
class MailForm(forms.Form):
    email=forms.EmailField()
    subject=forms.CharField(max_length=100)
    message=forms.CharField(
        max_length=50,
        widget=forms.Textarea(attrs={'rows':3,'col':30})
    )