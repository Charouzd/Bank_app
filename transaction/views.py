from django.shortcuts import render,redirect
from authentification.models import Account
import random
from random import randint
from . import methods
from django.contrib import messages
from .models import Transaction
def transfer(request):
    if request.user.is_authenticated:
        user=request.user
        user_extension = Account.objects.get(user=user)
        course=methods.new_dataset('transaction/cnb.txt')
        if(randint(0,1)==0):# 1 send; 0 recieve
            curr= random.choice((list)(course.keys()))
            rnd=(float)(randint(1,9999))
            payment={curr:rnd}
            if not methods.send(payment,user_extension,course) :
                messages.error(request, 'With deep regrets we have to inform you, that your transaction  - '+(str(rnd))+curr+' was canceled due to lack of capital')
            else:
                messages.success(request,'Your payment '+(str(rnd))+curr+' was compleated succesfully')
            # user_extension.Currencies=methods.get_dict_of_used_currencies(user_extension.Currencies)
            # user_extension.save()
        else:
            curr= random.choice((list)(course.keys()))
            rnd=(float)(randint(1,9999))
            payment={curr:rnd}
            
            if not methods.recieve(payment,user_extension,course):
                messages.error(request, 'With deep regrets we have to inform you, that your transaction -'+(str(rnd))+curr+' was canceled due to lack of capital')  
            else:
                messages.success(request,"Your account just recieved "+(str(rnd))+curr)
        return redirect("profile")
    else:
        return redirect('signin')
def donate(request):
    if request.user.is_authenticated:
        user=request.user
        user_extension = Account.objects.get(user=user)
        user_extension.CZK+=round(10000.0,2)
        user_extension.Currencies={"USD":round(1254.0,2),"EUR":round(159753.0,2),"PLN":round(666.69,2)}
        user_extension.save()
        return redirect('profile')
    else:
        return redirect('signin')
    
def history(request):
    try:
        account = Account.objects.get(user=request.user)
        history = account.history.all()
        transaction_list = [transaction.__str__() for transaction in history]
        return render(request,"transfer/history.html",{"trans":transaction_list})
    except:
        return redirect("home")
    
