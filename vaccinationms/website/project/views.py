import email
import re
from typing import final
from unittest import result
from urllib.parse import urldefrag
from webbrowser import get
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, authenticate, logout
import random ,smtplib , ssl
import mysql.connector as sql
from django.contrib import messages
from .models import Users ,searchByPinorDistrinct , appointmentDetails
from django.core.mail import send_mail

# Create your views here.
MESSAGE_TAGS = {
    messages.INFO: '',
    50: 'critical',
}
# Create your views here.
em=""
otp=str(random.randint(1000,9999))
final_otp=otp


def homepage_action(request):
     return render(request,'VMS1.html')


def signaction(request):
    if request.method=="POST":
        d=request.POST
        for key,value in d.items():
            if key=="first_name":
                fn=value
            if key=="last_name":
                ln=value
            if key=="gender":
                s=value
            if key=="email":
                em=value
            if key=="aadhar":
                aad=value
            if key=="psw":
                pwd=value
        
        result=Users.objects.filter(email=em , aadhar=aad)
        if len(result)!=0:
            messages.add_message(request,messages.INFO,'User already exists')
        else:
            usersave=Users()
            usersave.first_name=fn
            usersave.last_name=ln
            usersave.sex=s
            usersave.email=em
            usersave.aadhar=aad
            usersave.password=pwd
            usersave.save()
            des=""
            if s  =='male':
                des="Mr."
            else:
                des="Miss."
            messages.add_message(request,messages.INFO,'{}, {} Your Registration is Successful'.format( des, fn))
    return render(request,'register_page.html')


def loginaction(request):
    if request.method == "GET":
        # getting cookies
        if 'email' in request.COOKIES:
            context = {
                'email':request.COOKIES['email']
               
            }
            return render(request, 'login_page.html', context)
        else:
            return render(request, 'login_page.html')

    if request.method=="POST":
        em=request.POST.get('email')
        resultlogin=Users.objects.filter(email=em)
        if len(resultlogin)==0:
           messages.error(request,messages.INFO,'User Not Found')
           return render(request,'login_page.html')
        else:          
            send_otp(em,otp)
            context={
                'email':em 
            }
            messages.add_message(request,messages.INFO,'otp sent , Please check you inbox  ')
            #response=HttpResponse("otp sent , Please check you spam folder ")
            #response=render(request,'otp_page.html',context)
            response=redirect('/otp_login/')
            response.set_cookie('email',em)
            return response 
            #return redirect('/otp_login')
            #return render(request,'otp_page.html')
    return render(request,'login_page.html')
    



def send_otp(em,otp):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    sender='vaccinationms@gmail.com'
    password="obcumkveozaurwtk"
    server.login(sender,password)
    text='Hello,your otp is '+str(otp)
    sub="COVIESAFE VACCINATION"
    msg='Subject: {}\n\n{}'.format(sub, text)
    receiver=em
    server.sendmail(sender,receiver,msg)
    server.quit()
    context = {'message' : 'OTP is sent' }
    return HttpResponse(context)



def otpaction(request):
    if request.method == 'POST':
        otp1 = request.POST.get('enterotp')
        if otp1 != final_otp:
            messages.add_message(request,messages.INFO,'Wrong otp')
            return render(request,'otp_page.html')
        else:
            em=""
            item=""
            if 'email' in request.COOKIES:
                em=request.COOKIES['email']
            result=Users.objects.filter(email=em).values('first_name')
            for p in result:
                item=p['first_name']
           # print(item)
            context = {'message' : item }
            #messages.add_message(request,messages.INFO,'Welcome {} !!'.format(item))
            #return render(request , 'adminindex.html')
            return render(request,'adminindex.html',context)
    return render(request,'otp_page.html')

def adminIN(request):
    em=request.COOKIES['email']
    result=Users.objects.filter(email=em).values('first_name')
    for p in result:
        item=p['first_name']
    context={'message':item}
    return render(request,'adminindex.html',context)

def faq_action(request):
     return render(request,'faq1.html')

def faq_action1(request):
     return render(request,'faq2.html')


def vaccine(request):
    if request.method=='POST':
        if request.POST.get('pin'):
            pin=request.POST.get('pin')
            #print(pin)
            result=searchByPinorDistrinct.objects.filter(pin_code=pin).values('hospital_name')
            print(result)
            if len(result)==0:
                context={
                    "otpmessages":"Pin not found"
                }
                return render(request,'Vaccine.html', context)
            else:
                return render(request,'book_slot.html', {"searchByPinorDistrinct":result})
                
        elif request.POST.get('dist'):
            dist=request.POST.get('dist')
            result=searchByPinorDistrinct.objects.filter(District_name=dist).values('hospital_name')
            return render(request,'book_slot.html',{'searchByPinorDistrinct': result})
    else:
        return render(request,'Vaccine.html')
    return render(request,'Vaccine.html')


def bookSlot(request):
    if request.method=="POST":
        d=request.POST
        for key,value in d.items():
            if key=="Hospital":
                hospital=value
            if key=="dateV":
                dateV=value
            if key=="timeV":
                timeV=value
            if key=="email":
                em=value
            if key=="aadhar":
                aad=value
            if key=="psw":
                pwd=value
        
        em=request.COOKIES['email']
        result1=appointmentDetails.objects.filter(email=em)
        if len(result1)==0:
            result=appointmentDetails()
            result.email=em
            result.hospital_name=hospital
            result.Date=dateV
            result.Time=timeV
            result.save()

            server=smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            sender='vaccinationms@gmail.com'
            password="obcumkveozaurwtk"
            server.login(sender,password)
            text='YOUR APPIONTMENT IS SCHEDULED ON '+str(dateV)+' Between '+str(timeV)
            sub="COVIESAFE VACCINATION APPOINTMENT"
            msg='Subject: {}\n\n{}'.format(sub, text)
            receiver=em
            server.sendmail(sender,receiver,msg)
            server.quit()
            messages.add_message(request,messages.INFO,'Your Booking is Successful')
            return render(request,'Vaccine.html')
        else:
             messages.add_message(request,messages.INFO,'You have already booked slot for your vaccination')
             return render(request,'Vaccine.html')
    return render(request,'book_slot.html') 

def personalDetails(request):
     em=request.COOKIES['email']
     result=Users.objects.filter(email=em)
     return render(request,'cust_dashboard.html',{'Users':result})

def appoint(request):
    em=request.COOKIES['email']
    result=appointmentDetails.objects.filter(email=em)
    if len(result)==0:
        messages.add_message(request,messages.INFO,'NO APPOINTMENT SCHEDULED')
        return render(request,'appoint.html')
    else:
        return render(request,'appoint.html',{'appointmentDetails':result})


def logout(request):
    response= HttpResponseRedirect(reverse('homepage'))
    response.delete_cookie('email')

    return response


def cancel(request):
    if request.method=='POST':
        em=request.COOKIES['email']
        result=appointmentDetails.objects.filter(email=em).values('Date')
        dateV=""
        for d in result:
            dateV=d['Date']
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        sender='vaccinationms@gmail.com'
        password="obcumkveozaurwtk"
        server.login(sender,password)
        text='YOUR APPIONTMENT ON '+str(dateV)+' IS CANCELLED'
        sub="COVIESAFE VACCINATION APPOINTMENT"
        msg='Subject: {}\n\n{}'.format(sub, text)
        receiver=em
        server.sendmail(sender,receiver,msg)
        server.quit()
        result=appointmentDetails.objects.get(email=em).delete()
        messages.add_message(request,messages.INFO,'BOOKING CANCELED')
        return render(request,'appoint.html')
    return render(request,'appoint.html')



def contactus(request):
    return render(request,'contactus.html')