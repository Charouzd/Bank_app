from authentification.models import Account
from django.contrib.auth.models import User
from .models import Transaction

def recieve(payment, account, currency):
    # Get the currency and value from the payment dictionary
    payment_currency, payment_value = list(payment.items())[0]
    transaction = Transaction.objects.create(account=account.user,direction='in', currency=payment_currency, amount=payment_value)
    # Check if the account has the payment currency
    if payment_currency in account.Currencies:
        account.Currencies[payment_currency] += payment_value
        transaction.status=True
        transaction.save()
        account.history.add(transaction.id)
        account.save()
        return True
    else:
        # Convert the payment into CZK using the currency dictionary
        czk_value = convert_currency(payment_currency, payment_value, currency)
        account.CZK += czk_value
        account.CZK=round(account.CZK,2)
        transaction.status=True
        transaction.save()
        account.history.add(transaction.id)
        account.save()
        return True
    return False

def send(payment, account, currency):
    # Get the currency and value from the payment dictionary
    payment_currency, payment_value = list(payment.items())[0]
    transaction = Transaction.objects.create(account=account.user,direction='out', currency=payment_currency, amount=payment_value)
    # Check if the account has enough of the payment currency
    if payment_currency in account.Currencies and account.Currencies[payment_currency] >= payment_value:
        account.Currencies[payment_currency] -= payment_value
        transaction.status=True
        transaction.save()
        account.history.add(transaction.id)
        account.save()
        return True
    else:
        # Convert the payment into CZK using the currency dictionary
        if payment_currency in currency:
            czk_value = payment_value * currency[payment_currency]
            if account.CZK >= czk_value:
                account.CZK -= czk_value
                account.CZK=round(account.CZK,2)
                transaction.status=True
                transaction.save()
                account.history.add(transaction.id)
                account.save()
                return True
    transaction.status=False
    transaction.save()
    account.history.add(transaction.id)
    account.save()
    return False
    
def new_dataset(file_path):
    with open(file_path,"r",encoding="utf8")as f:
        raw_data=f.read() # data+heading
        tmp=raw_data.split('\n')
        tmp.pop(0)
        tmp.pop(0)
        courses={}
        for line in tmp:#unseparated data
            temp=line.split('|')#separated data in form (0)země,(1)měna,(2)množství,(3)kód,(4)kurz
            cur=temp[3]
            val=(float)(temp[4].replace(",","."))
            if tmp[2] != "1":
                x=float(temp[4].replace(",","."))
                y=float(temp[2].replace(",","."))
                val=x/y
            courses[cur]= val
        courses.update({'CZK':1})
    return courses
def get_dict_of_used_currencies(curr):
    return {k: v for k, v in curr.items() if v != 0}

def convert_currency(from_currency, from_value, currency_rates):
    to_currency = 'CZK'
    if from_currency == to_currency:
        return from_value
    elif from_currency not in currency_rates or to_currency not in currency_rates:
        return None
    else:
        exchange_rate = currency_rates[to_currency] / currency_rates[from_currency]
        to_value = from_value * exchange_rate
        return to_value
def convert_possible(x,y):
    if x>=y:
        return True
    return False
def delete_history(account):
    # Assume `account` is an existing Account instance
    account.history.clear()

    # Check if transactions have been cleared
    if account.history.exists():
        return False
    else:
        return True
