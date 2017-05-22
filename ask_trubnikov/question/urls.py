from django.conf.urls import url
from question import views

urlpatterns = [
    url(r'logout/$', views.v_logout, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^hot/$', views.hot, name='hot'),
    url(r'^tag/([A-z]+)/$', views.tag, name='tag'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.question, name='question'),
    url(r'login/$', views.v_login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^ask/$', views.ask, name='ask'),

    # url(r'^tag/(.*)/$', views.tag, name='rus_tag'),  # rus char, kak sdelat' normal'no?
]
