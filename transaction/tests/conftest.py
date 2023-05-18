import pytest
from django.contrib.auth.models import User
from authentification.models import Account
from transaction.models import Transaction
from transaction.methods import *



@pytest.fixture
def user_login_data():
    return { 'username': 'bambino','pass1': '3210'}
@pytest.fixture
def user_data():
    return { 'username': 'bambino','first_name':'Abu','last_name':'Dhabe','email': 'sibik@seznam.cz','password': '3210'}
@pytest.fixture
def user_create_data():
    return { 'username': 'bambino','fname':'Abu','lname':'Dhabe','email': 'sibik@seznam.cz','pass1': '3210', 'pass2': '3210',}
@pytest.fixture
def authenticated_user(client, user_data):
    test_user = User.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    test_user.save()
    client.login(**user_data)
    test_account = Account.objects.create(user=test_user)
    test_account.save()

    return test_user
@pytest.fixture
def payment(client,user_data):
    p={"USD":3}
    test_user = User.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    test_user.save()
    client.login(**user_data)
    test_account = Account.objects.create(user=test_user)
    test_account.CZK=25000
    test_account.save()
    cur={
        "USD":20,
        "EUR":10,
        "CZK":1
    }
    send(p,test_account,cur)
    return { 'payment':p ,'account':test_account,"currency":cur}
@pytest.fixture
def fpayment(client,user_data):
    p={"USD":3000}
    test_user = User.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    test_user.save()
    client.login(**user_data)
    test_account = Account.objects.create(user=test_user)
    test_account.CZK=25
    test_account.save()
    cur={
        "USD":20,
        "EUR":10,
        "CZK":1
    }
    return { 'payment':p ,'account':test_account,"currency":cur}