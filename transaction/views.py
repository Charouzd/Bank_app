from django.shortcuts import render,redirect
from authentification.models import Account
import random
from random import randint
from . import methods
from django.contrib import messages
def transfer(request):
    user=request.user
    user_extension = Account.objects.get(user=user)
    course=methods.new_dataset('transaction/cnb.txt')
    if(randint(0,1)==0):# 1 send; 0 recieve
        curr= random.choice((list)(course.keys()))
        rnd=randint(1,9999)
        payment={curr:rnd}
        if not methods.send(payment,user_extension,course) :
            messages.error(request, 'With deep regrets we have to inform you, that your transaction  - '+(str(rnd))+curr+' was canceled due to lack of capital')
        else:
            messages.success(request,'Your payment '+(str(rnd))+curr+' was compleated succesfully')
        # user_extension.Currencies=methods.get_dict_of_used_currencies(user_extension.Currencies)
        # user_extension.save()
    else:
        curr= random.choice((list)(course.keys()))
        rnd=randint(1,9999)
        payment={curr:rnd}
        
        if not methods.recieve(payment,user_extension,course):
             messages.error(request, 'With deep regrets we have to inform you, that your transaction -'+(str(rnd))+curr+' was canceled due to lack of capital')  
        else:
            messages.success(request,"Your account just recieved "+(str(rnd))+curr)
    return redirect("profile")
def donate(request):
    user=request.user
    user_extension = Account.objects.get(user=user)
    user_extension.CZK=20000
    user_extension.Currencies={"USD":1254,"EUR":159753,"PLN":666}
    user_extension.save()
    return redirect('profile')
