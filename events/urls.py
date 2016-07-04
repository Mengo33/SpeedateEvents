from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import views

app_name = "events"
urlpatterns = [
    url(r'^$', views.ListUserView.as_view(), name="user_list"),
    url(r'^home/$', TemplateView.as_view(template_name='events/index.html'), name="home"),
    url(r'^event-list/$', views.ListEventView.as_view(), name="event_list"),
    url(r'^add-event/$', views.CreateEventView.as_view(), name="create_event"),
    url(r'^(?P<pk>\d+)/$', views.EventDetailView.as_view(), name="event_details"),
    # url(r'^(?P<pk>\d+)/add-reply/$', views.CreateReplyView.as_view(), name="create_reply"),
    # url(r'^(?P<pk>\d+)/reply_details/$', views.ReplyDetailView.as_view(), name="reply_details"),
    # url(r'^view-singles/$', views.ListsinglesView.as_view(), name="singles_list"),
]
