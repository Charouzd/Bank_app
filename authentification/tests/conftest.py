import pytest
from django.contrib.auth.models import User
from authentification.models import Account

@pytest.fixture
def fuser_login_data():
    return { 'username': 'bambino','pass1': '321022'}
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
def fuser_create_data():
    return { 'username': 'bambino','fname':'Abu','lname':'Dhabe','email': 'sibik@seznam.cz','pass1': '3210', 'pass2': '32f10',}
@pytest.fixture
def num_user_create_data():
    return { 'username': '!!?L$','fname':'Abu','lname':'Dhabe','email': 'sibik@seznam.cz','pass1': '3210', 'pass2': '3210',}


@pytest.fixture
def create_test_user(user_data):
    test_user = User.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    return test_user
@pytest.fixture
def create_test_account(my_user):
    test_account = Account.objects.create(user=my_user)
    return test_account

@pytest.fixture
def authenticated_user(client, user_data):
    test_user = User.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    test_user.save()
    client.login(**user_data)
    test_account = Account.objects.create(user=test_user)
    test_account.save()

    return test_user