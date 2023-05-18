from django import urls
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from authentification.models import Account
import pytest

@pytest.mark.parametrize('param',[('home'),('signup'),('signin'),('change')])
@pytest.mark.parametrize('param1',[('profile'),('signout')])
def test_render_views(client, param,param1):
	temp_url = urls.reverse(param)
	temp_url1 = urls.reverse(param1)
	resp1=client.get(temp_url1)
	assert resp1.status_code == 302	
	resp = client.get(temp_url)
	assert resp.status_code == 200
 
@pytest.mark.django_db
def test_sign_up_succes(client,user_create_data):
	user_model= User.objects.count()
	account_model=Account.objects.count()
	assert user_model==0
	assert account_model==0
	signup_url = urls.reverse('signup')
	resp = client.post(signup_url,user_create_data)
	user_m= User.objects.exists()
	account_model=Account.objects.count()
	assert user_m==True
	assert account_model==1
	assert resp.status_code == 302
 
@pytest.mark.django_db
def test_sign_up_fail(client,fuser_create_data):
	user_model= User.objects.count()
	account_model=Account.objects.count()
	assert user_model==0
	assert account_model==0
	signup_url = urls.reverse('signup')
	resp = client.post(signup_url,fuser_create_data)
	user_m= User.objects.exists()
	account_model=Account.objects.count()
	assert user_m==False
	assert account_model==0
	assert resp.status_code == 302
 
@pytest.mark.django_db
def test_sign_up_all_num_fail(client,num_user_create_data):
	user_model= User.objects.count()
	account_model=Account.objects.count()
	assert user_model==0
	assert account_model==0
	signup_url = urls.reverse('signup')
	resp = client.post(signup_url,num_user_create_data)
	user_m= User.objects.exists()
	account_model=Account.objects.count()
	assert user_m==False
	assert account_model==0
	assert resp.status_code == 302

@pytest.mark.django_db
def test_user_login_succes(client, create_test_user, user_data,user_login_data):
	assert User.objects.count() == 1
	login_url = urls.reverse('signin')
	resp = client.post(login_url, data=user_login_data)
	assert resp.status_code == 200
	assert 'authentification/verify.html' in [template.name for template in resp.templates]
 
@pytest.mark.django_db
def test_user_login_fail(client, create_test_user, user_data,fuser_login_data):
	assert User.objects.count() == 1
	login_url = urls.reverse('signin')
	resp = client.post(login_url, data=fuser_login_data)
	assert resp.status_code == 302
	assert resp.url == urls.reverse('signin')

@pytest.mark.django_db
def test_user_logout(client, authenticated_user):
	logout_url = urls.reverse('signout')
	resp = client.get(logout_url)
	assert resp.status_code == 302
	assert resp.url == urls.reverse('home')
 
@pytest.mark.django_db
def test_user_profile_logged_user(client, authenticated_user):
	profile_url = urls.reverse('profile')
	resp = client.get(profile_url)
	assert resp.status_code == 200
	assert 'account.html' in [template.name for template in resp.templates]
 
@pytest.mark.django_db
def test_user_profile_unlogged_user(client):
	profile_url = urls.reverse('profile')
	resp = client.get(profile_url)
	assert resp.status_code == 302
	assert resp.url == urls.reverse('signin')
 
@pytest.mark.django_db
def test_user_profile_change_(client):
	profile_url = urls.reverse('change')
	resp = client.get(profile_url)
	assert resp.status_code == 200
	assert 'authentification/signin.html' in [template.name for template in resp.templates]