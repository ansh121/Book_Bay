# template tags used for books

from django import template

register = template.Library()

# a partial view of a single book as
# seen by the owner

# returns the book id, title and author of 'book'

# TODO: check the status of the book
# and add classes to color the book block
# and other logic?

@register.inclusion_tag('books/book_private.html')
def show_book_private(book):
	return {
		'book_id': book.id,
		'book_title': book.title,
		'book_author': book.author,
		'summary' : book.summary,
	}

# this tag allows the viewer to request the book/
# etc - as seen by a non-owner
@register.inclusion_tag('books/book_public.html')
def show_book_public(book):
	return {
		'book_id': book.id,
		'book_title': book.title,
		'book_author': book.author,
		'book_owner': book.owner,
		'summary' : book.summary,
	}
