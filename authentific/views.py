from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
#from django.core.mail import EmailMessage, send_mail
#from bank_app import settings
#from django.contrib.sites.shortcuts import get_current_site
#from django.template.loader import render_to_string
#from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
#from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
#from . tokens import generate_token

# Create your views here.
def homepage(request):
    return render(request,"index.html")
def loggin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('/homepage')
    return render(request,"loggin.html")
def register(request):
    
    if request.method == "POST":
        account_name = "filip" #request.POST['name']
        account_number ="123" #request.POST['username']
        account_password ="123" #request.POST['password']
        account_mail = request.POST['mail']
        # if User.objects.filter(username=account_number):
        #     messages.error(request, "Username already exist! Please try some other username.")
        #     return redirect('homepage')
        
        # if User.objects.filter(email=account_mail).exists():
        #     messages.error(request, "Email Already Registered!!")
        #     return redirect('homepage')
        
        # if len(account_number)>20:
        #     messages.error(request, "Username must be under 20 charcters!!")
        #     return redirect('homepage')
        myuser = User.objects.create_user(account_number, "filip@hah.cz", account_password)
        myuser.name = account_name
        myuser.is_active = False
        myuser.save()
        #messages.success(request, "Your Account has been created succesfully!!")
        return redirect(request,' ')
        
    return render(request,"register.html")

    