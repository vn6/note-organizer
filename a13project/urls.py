"""a13project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from json.decoder import JSONDecodeError
from django import urls
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView


from django.http import HttpResponse, HttpResponseRedirect

from django.views import generic
import requests
from django.template import loader

class IndexView(generic.View):
    def index(request):
        template = loader.get_template('index.html')
        quoteText=""
        quoteAuthor=""

        while True:
            try:
                response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
                quote = response.json()
                quoteText = quote['quoteText']
                quoteAuthor = quote['quoteAuthor']
            except JSONDecodeError: #for some reason this api returns lots of decode errors
                continue
            break
        context = {
            'quoteText': quoteText,
            'quoteAuthor': quoteAuthor
        }
        return HttpResponse(template.render(context, request))

urlpatterns = [
    path('organizer/', include('organizer.urls')),  # the app is called organizer so it's intuitive in url
    path('admin/', admin.site.urls),
    path('', IndexView.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)