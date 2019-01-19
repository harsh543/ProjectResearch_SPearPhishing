from django.http import HttpReesponse
from django.contrib.auth.decorators import login_required

def public(request):
    return HttpResponse("Welcome to public page")


@login_required
def private(request):
    return HttpResponse("Welcome to private page") 
