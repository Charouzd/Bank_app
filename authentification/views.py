from django.shortcuts import redirect, render
from django.http import HttpResponse,request
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from bank_app import settings
from .models import Account
from .token import account_activation_token
from datetime import datetime

def profile(request):
    if request.user.is_authenticated:
        # User is already logged in, redirect to account page
        dic={
            "username": request.user.username,
            "fname": "user logged before",
            "lname": request.user.last_name,
            "mail": request.user.email,
            "lastlog":request.user.last_login,
            "czk": request.user.account.CZK,
            "currencies": request.user.account.Currencies,
        }
        return render(request, "account.html", dic)
    return redirect('signin')
    
def activate(request, uidb64, token):
    if request.user.is_authenticated:
        # User is already logged in, redirect to account page
        dic={
            "username": request.user.username,
            "fname": "user logged before",
            "lname": request.user.last_name,
            "mail": request.user.email,
            "czk": request.user.account.CZK,
            "currencies": request.user.account.Currencies,
        }
        return render(request, "account.html", dic)

    User = get_user_model()
    token_with_timestamp = token.split('--')
    dt = datetime.strptime(token_with_timestamp[1], '%Y-%m-%d %H:%M:%S')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if ((datetime.now()-dt).total_seconds() > 300):
            # Token has expired (300 seconds = 5 minutes)
            messages.error(request, "Activation link is expired!")
            return render(request, "authentification/signin.html")
    except User.DoesNotExist:
        user = None

    if user is not None and account_activation_token.check_token(user, token_with_timestamp[0]):
        user_extension = Account.objects.get(user=user)
        login(request, user)
        request.session['account_id'] = user.username
        dic={
            "username":user.username,
            "fname":user.first_name,
            "lname":user.last_name,
            "mail":user.email,
            "czk":user_extension.CZK,
            "currencies": user_extension.Currencies,
        }
        messages.success(request, "Thank you for your email confirmation. You are now logged in.")
        return render(request, "account.html", dic)
    else:
        messages.error(request, "Activation link is invalid! try to log in again please.")
        return redirect('signin')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    dt=datetime.now()
    message = render_to_string("authentification/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user) + '--' +dt.strftime('%Y-%m-%d %H:%M:%S'),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    logout(request)
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if your email is active.')


def home(request):
    return render(request,"index.html")
def sign_up(request):
    
    ## vytezovani requestu
    if request.method == "POST":
        username = request.POST.get("username")
        # Optional -> username = request.POST["username"]
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        fname = request.POST.get("fname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        
        ## Podminky pro uspesne vytvoreni uctu
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        ## vytvareni zapis do databaze
        my_user = User.objects.create_user(username,email,pass1)
        my_user.first_name=fname
        my_user.last_name=lname
        my_user.save()
        user_extension = Account(user=my_user)
        user_extension.Currencies = {"czk":0}
        user_extension.save()
        messages.success(request,"Your acount has been successfully created")
        ## Welcome Email
        subject = "Congratulations! you have successfully register your account"
        message = "Welccome " + fname + lname +  "!! \n" + "\nThank you for using our services\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Yours UniBank"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return redirect("signin")
    return render(request, "authentification/signup.html")

def sign_in(request):
    if request.method=="POST":
        uname = request.POST.get("username")
        pass1 = request.POST.get("pass1")
        user = authenticate(username=uname,password=pass1)
        if user is not None:
            activateEmail(request, user, user.email)
            return render(request,"authentification/verify.html",{"user":user.username, "mail": user.email} )
        else:
            messages.error(request,"Incorect password or username")
            return redirect("signin")
    return render(request, "authentification/signin.html")
def sign_out(request):
    logout(request)
    messages.success(request,"You has been successfully logged out")
    return redirect("home")
    # return render(request, "authentification/signout.html")
    