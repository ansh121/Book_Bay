from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from misc import anonymous_required

@anonymous_required
def index(request):
	return render(request, 'index.html')

@anonymous_required
def about(request):
	return render(request, 'about.html')

@anonymous_required
def contact(request):
	return render(request, 'contact.html')