# template tags used for book requests

from bookrequests.models import BookRequest

from django.db.models import Q

from django import template

register = template.Library()

# request tracking by the owner of a book
# 1. accept/reject request
# 2. pending pickup
# 3. with courier, going to borrower
# 4. with borrower
# 5. borrower finished reading
# 6. with courier, coming back
# 7. completed

@register.inclusion_tag('bookrequests/request_owner.html')
def show_request_owner(req):
	borrower = str(req.borrower)
	title = str(req.book.title)
	author = str(req.book.author)

	messages = {
		BookRequest.REQUEST_MADE:
			 "{0} sent you a request for {1}",
		BookRequest.REQUEST_ACCEPTED:
			 "Accepted request by {0} for {1}",
		BookRequest.REQUEST_REJECTED:
			 "Rejected request by {0} for {1}",
		BookRequest.WITH_COURIER_TO_BORROWER:
			"Your book {1} is being sent to {0}", 
		BookRequest.WITH_BORROWER:
			"Your book {1} is with {0}", 
		BookRequest.DONE_READING:
			"{0} has finished reading your book {1}", 
		BookRequest.WITH_COURIER_TO_OWNER:
			"Your book {1} is being sent back to you from {0}", 
		BookRequest.RETURNED:
			"{1} has been returned by {0}", 
	}

	accept_buttons = (req.status == BookRequest.REQUEST_MADE)

	return {
		'request_id': req.id,
		# add the borrower and title into the message
		'message': messages[req.status].format(borrower, title),
		'accept_buttons': accept_buttons
	}

# request tracking by the borrower of a book
@register.inclusion_tag('bookrequests/request_borrower.html')
def show_request_borrower(req):
	owner = str(req.book.owner)
	title = str(req.book.title)
	author = str(req.book.author)

	messages = {
		BookRequest.REQUEST_MADE:
			 "{0} is yet to approve your request for {1}",
		BookRequest.REQUEST_ACCEPTED:
			 "{0} has accepted your request for {1}",
		BookRequest.REQUEST_REJECTED:
			 "{0} has rejected your request for {1}",
		BookRequest.WITH_COURIER_TO_BORROWER:
			"{0} has handed over {1} to the courier", 
		BookRequest.WITH_BORROWER:
			"{0}'s book {1} is with you", 
		BookRequest.DONE_READING:
			"Our courier will pick up {1} from you shortly", 
		BookRequest.WITH_COURIER_TO_OWNER:
			"{1} is being sent back to {0}", 
		BookRequest.RETURNED:
			"You have returned {1} to {0}", 
	}

	return_button = (req.status == BookRequest.WITH_BORROWER)

	return {
		'request_id': req.id,
		# add the borrower and title into the message
		'message': messages[req.status].format(owner, title),
		'return_button': return_button
	}

# request tracking by the courier
@register.inclusion_tag('bookrequests/request_courier.html')
def show_request_courier(req):
	messages = {
		BookRequest.REQUEST_ACCEPTED:
			"Pick up {title} from {name}, {addr}".format(
				title=req.book.title,
				name=req.book.owner.username,
				addr=req.book.owner.userinfo.address),
		BookRequest.DONE_READING:
			"Pick up {title} from {name}, {addr}".format(
				title=req.book.title,
				name=req.borrower.username,
				addr=req.borrower.userinfo.address),

		BookRequest.WITH_COURIER_TO_BORROWER:
			"Drop off {title} to {name}, {addr}".format(
				title=req.book.title,
				name=req.borrower.username,
				addr=req.borrower.userinfo.address),
	
		BookRequest.WITH_COURIER_TO_OWNER:
			"Drop off {title} to {name}, {addr}".format(
				title=req.book.title,
				name=req.book.owner.username,
				addr=req.book.owner.userinfo.address),

		BookRequest.WITH_BORROWER:
			"Dropped off {title} to {name}, at {addr}".format(
				title=req.book.title,
				name=req.borrower.username,
				addr=req.borrower.userinfo.address),
		BookRequest.RETURNED:
			"Dropped off {title} to {name}, at {addr}".format(
				title=req.book.title,
				name=req.book.owner.username,
				addr=req.book.owner.userinfo.address),
	}

	# show the confirm button when there is something to be 
	# done (pick/drop)
	confirm_button = (req.status not in (
			BookRequest.WITH_BORROWER,
			BookRequest.RETURNED,
		))

	return {
		'message': messages[req.status],
		'req_id': req.id,
		'confirm_button' : confirm_button
	}	


# template filters

# returns the pending requests from a queryset 
# of requests
@register.filter
def pending(queryset):
	return queryset.filter(Q(status=BookRequest.REQUEST_MADE)
						|  Q(status=BookRequest.WITH_BORROWER)
						|  Q(status=BookRequest.REQUEST_ACCEPTED)
						|  Q(status=BookRequest.DONE_READING))


# returns the completed requests from a queryset 
# of requests
@register.filter
def completed(queryset):
	return queryset.filter(Q(status=BookRequest.RETURNED)
						|  Q(status=BookRequest.REQUEST_REJECTED))

# returns the requests with courier from a queryset 
# of requests
@register.filter
def intransit(queryset):
	return queryset.filter(Q(status=BookRequest.WITH_COURIER_TO_BORROWER)
						|  Q(status=BookRequest.WITH_COURIER_TO_OWNER))	


@register.filter
def courier_pending(queryset):
	return queryset.filter(Q(status=BookRequest.REQUEST_ACCEPTED)
						|  Q(status=BookRequest.DONE_READING)
						|  Q(status=BookRequest.WITH_COURIER_TO_BORROWER)
						|  Q(status=BookRequest.WITH_COURIER_TO_OWNER))


@register.filter
def courier_completed(queryset):
	return queryset.filter(Q(status=BookRequest.RETURNED)
						|  Q(status=BookRequest.WITH_BORROWER))
