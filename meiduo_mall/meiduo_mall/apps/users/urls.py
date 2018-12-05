from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user_detail/$', views.UserDetailView.as_view()),
    url(r'^email/$', views.EmailView.as_view()),
]
