"""

date: 18-12-10 下午3:05
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^action/$", views.CartView.as_view()),
]
