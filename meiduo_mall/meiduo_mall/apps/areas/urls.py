from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/(?P<parent>\d+)/$', views.AreaListView.as_view()),
]
