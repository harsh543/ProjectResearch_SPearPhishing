from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login
from . import views


urlpatterns = [
        url(r'^admin/',admin.site.urls),
        url(r'^login/$',login,name='login'),
        url(r'^public/',views.public,name='public'),
        url(r'^private/',views.private,name='private'),
        
     ]
