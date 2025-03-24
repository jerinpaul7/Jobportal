from django.urls import path
from .views import *
urlpatterns=[path('login/',u_login),
             path('',home),
             path("register/",registerpage),
             path('clogin/',c_login),
             path('cregister/',c_register),
             path('edit/<int:id1>',edituser),
             path('updateuser/<int:id>',update),
             path('verify/<auth_token>',verify),
             path('error/',error),
             path('postform/<int:id>',postfo),
             path('showjobs/<int:id1>',showjob),
             path('about/', about),
             path('apply/<int:id>/<int:userid>/', applypage, name="applypage"),
             path('appliedjobs/<int:id1>', aplliedjobs1, name='appliedjobs1'),

             path('viewapplied/<int:id>',viewapplied),
             path('viewcompany/',viewcompany),
             path('sendmail/<int:id>/',sendmail),
             path('userprofile/<int:userid>/',userprofile, name='userprofile'),

             ]