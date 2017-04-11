from django.conf.urls import url
from questions import views

urlpatterns = [
    url(r'^hello$', views.hello_world, name='HelloWorld'),
    url(r'^template.html$', views.template, name='example_html'),
    url(r'^.*/', views.reqGetPost, name='GetPost')
]
