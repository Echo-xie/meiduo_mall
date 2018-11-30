from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^test/', views.test),
    url(r'^cross_domain_test/', views.cross_domain_test.as_view()),
]
