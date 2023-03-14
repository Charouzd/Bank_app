from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
#from bank_app import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
#from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
#from . tokens import generate_token

# Create your views here.
def homepage(request):
    return render(request,"index.html")
def loggin(request):
    
    if request.method == "POST":
        account_number = request.POST['username']
        account_password = request.POST['password']
        
        user=authenticate(username=account_number,password=account_password)
        if user is not None:
            login(request,user)
            render(request,"accountscreen.html",{"name":user.first_name(),"mail":user.mail,"money":user.czk})
        else:
            messages.error(request,"incorect account number or password")
            return redirect('loggin')
    
    
    return render(request,"loggin.html")
def register(request):
    
    if request.method == "POST":
        account_name = request.POST['name']
        account_number = request.POST['username']
        account_password = request.POST['password']
        account_mail = request.POST['mail']
        if User.objects.filter(username=account_number):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('')
        
        if User.objects.filter(email=account_mail).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('')
        
        if len(account_number)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('')
        myuser = User.objects.create_user(account_number, account_mail, account_password)
        myuser.first_name = account_name
        myuser.czk=0
        myuser.mail=account_mail
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        return render(request,'index.html')
    return render(request,"register.html")

    