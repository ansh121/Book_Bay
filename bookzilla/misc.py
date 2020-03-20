# misc functions

from django.http import HttpResponseRedirect

# A decorator to redirect logged-in users from login, register pages
# from http://stackoverflow.com/questions/2320581/django-redirect-logged-in-users-from-login-page
# redirects a logged in users to bookzilla.settings.LOGIN_REDIRECT_URL

def anonymous_required( view_function, redirect_to = None ):
    return AnonymousRequired( view_function, redirect_to )

class AnonymousRequired( object ):
    def __init__( self, view_function, redirect_to ):
        if redirect_to is None:
            from django.conf import settings
            redirect_to = settings.LOGIN_REDIRECT_URL
        self.view_function = view_function
        self.redirect_to = redirect_to

    def __call__( self, request, *args, **kwargs ):
        if request.user is not None and request.user.is_authenticated():
            return HttpResponseRedirect( self.redirect_to )
        return self.view_function( request, *args, **kwargs )