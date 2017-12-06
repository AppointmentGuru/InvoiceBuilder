"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from invoice.api import router
from invoice import views

urlpatterns = [
    url(r'^bulk/preview/(?P<practitioner>[0-9]+)/(?P<from_date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/(?P<to_date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/', views.invoices, name='invoices_preview'),
    url(r'^invoice/preview/', views.preview, name='invoice_preview'),
    url(r'^invoice/(?P<pk>[0-9]+)/', views.invoice, name='invoice_view'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
