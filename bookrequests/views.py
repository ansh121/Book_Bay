from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

# models
from books.models import Book
from .models import BookRequest

@login_required
def lent_index(request):
	user = request.user
	requests = BookRequest.objects.all().filter(book__owner=user)

	# get requests where the owner is 'user'
	# my_lent = (r for r in requests if r.book.owner == user)

	return render(request,
				'bookrequests/lent_index.html', 
				{
					'requests': requests
				})

@login_required
def borrowed_index(request):
	user = request.user
	requests = BookRequest.objects.all().filter(borrower=user)

	# get requests where the borrower is 'user'
	# my_borrowed = (r for r in requests 
	# 					if r.borrower == user)

	return render(request,
				'bookrequests/borrowed_index.html', 
				{
					'requests': requests
				})

@login_required
def accept(request, id):
	req = get_object_or_404(BookRequest, pk=id)
	
	req.status = BookRequest.REQUEST_ACCEPTED
	req.save()

	return HttpResponseRedirect(reverse('users:requests:lent'))

@login_required
def reject(request, id):
	req = get_object_or_404(BookRequest, pk=id)	

	req.status = BookRequest.REQUEST_REJECTED
	req.save()
	
	return HttpResponseRedirect(reverse('users:requests:lent'))	

@login_required
def return_book(request, id):
	req = get_object_or_404(BookRequest, pk=id)	

	req.status = req.next_status()
	req.save()
	
	return HttpResponseRedirect(reverse('users:requests:borrowed'))	


