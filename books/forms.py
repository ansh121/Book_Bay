# contains forms needed for creating, editing a book
# and other functions

from django import forms

class EditBookForm(forms.Form):
	title = forms.CharField(label='Title')
	author = forms.CharField(label='Author')
	summary = forms.CharField(label='Summary',
				required=False,
				widget=forms.Textarea(attrs=
					{'placeholder': 'Summary (upto 140 characters)'
					})
				)