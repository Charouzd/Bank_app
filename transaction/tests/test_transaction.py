from django import urls
from django.contrib.auth.models import User
from authentification.models import Account
from transaction.models import Transaction
import pytest
import transaction.methods as m


@pytest.mark.parametrize('param1',[('donate'),('transfer'),('history')])
def test_render_views(client,param1):
	temp_url1 = urls.reverse(param1)
	resp1=client.get(temp_url1)
	assert resp1.status_code == 302
 
# @pytest.mark.django_db
# def test_user_profile_transaction_succes(client, authenticated_user):
# 	profile_url = urls.reverse('transfer')
# 	transaction_test=Transaction.objects.exists()
# 	assert transaction_test == False
# 	resp = client.get(profile_url)
# 	assert resp.status_code == 302
# 	assert resp.url == urls.reverse('profile')
# 	transaction_test=Transaction.objects.exists()
# 	assert transaction_test == True
	
# @pytest.mark.django_db
# def test_user_profile_transaction_fail(client,):
# 	profile_url = urls.reverse('transfer')
# 	transaction_test=Transaction.objects.exists()
# 	assert transaction_test == False
# 	resp = client.get(profile_url)
# 	assert resp.status_code == 302
# 	assert resp.url == urls.reverse('signin')
 
# @pytest.mark.django_db
# def test_user_profile_donate_succes(client, authenticated_user):
# 	profile_url = urls.reverse('donate')
# 	resp = client.get(profile_url)
# 	assert resp.status_code == 302
# 	assert resp.url == urls.reverse('profile')

# @pytest.mark.django_db
# def test_logged_user_profile_history(client, authenticated_user):
# 	profile_url = urls.reverse('history')
# 	resp = client.get(profile_url)
# 	assert resp.status_code == 200
# 	assert 'transfer/history.html' in [template.name for template in resp.templates]

def test_convert_possible():
	assert m.convert_possible(10,20) ==False
	assert m.convert_possible(20,10) ==True
#def convert_currency(from_currency, from_value, currency_rates):
def test_cpnvert_currency_ok():
	d={
	"czk":1.0,
	"USD":25.0,
	"EUR":20.0	
	}
	tmp_val=m.convert_currency("USD",2.0,d)
	assert tmp_val==50
def test_cpnvert_currency_none():
	d={
	"czk":1.0,
	"USD":25.0,
	"EUR":20.0	
	}
	tmp_val=m.convert_currency("US",2.0,d)
	assert tmp_val==None
def test_cpnvert_currency_equal():
	d={
	"czk":1.0,
	"USD":25.0,
	"EUR":20.0	
	}
	tmp_val=m.convert_currency("czk",2.0,d)
	assert tmp_val==2.0
def test_new_dataset():
    dic=m.new_dataset("transaction/tests/testfile.txt")
    assert len(dic)==4
    dic2 =m.new_dataset("lol.txt")
    assert dic2==None

