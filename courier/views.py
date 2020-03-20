from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout

from .forms import LoginForm

from .misc import is_member

from bookrequests.models import BookRequest

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(username=username, password=password)

			if user is not None and is_member(user, 'Couriers'):
				djlogin(request, user)
				return HttpResponseRedirect(reverse('courier:home'))
			else:
				messages.error(request,
		     	'The username or password you entered is incorrect')

	form = LoginForm()
	return render(request, 'courier/index.html',
				{
					'form': form
				})

@login_required(login_url='/courier/login')
def home(request):
	requests = BookRequest.objects.all().exclude(status=BookRequest.REQUEST_REJECTED).exclude(status=BookRequest.REQUEST_MADE)

	return render(request, 'courier/home.html',
				{
					'requests' : requests
				})

@login_required(login_url='/courier/login')
def logout(request):
	djlogout(request)
	return HttpResponseRedirect(reverse('courier:login'))

@login_required(login_url='/courier/login')
def advance_request(request, req_id):
	req = get_object_or_404(BookRequest, pk=req_id)
	req.status = req.next_status()
	req.save()
	
	return HttpResponseRedirect(reverse('courier:home'))
