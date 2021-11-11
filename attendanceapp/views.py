from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello! Welcome to the Attendence Project website. Check out the <a href='/admin'>admin panel</a> and sign in with username 'test' and password 'test'.")
