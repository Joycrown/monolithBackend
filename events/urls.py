from django.urls import path
from rest_framework import routers


from events.views import EventViewSet, EventWhoAttendeMe

from events.views import EventListAPIView,JoinEventView

from events.views import EventAttendeesAPIView,FeedbackView,EventDetailView,FeedbackListView

router = routers.SimpleRouter()
router.register('myevent', EventViewSet, basename='event')


urlpatterns=[
    path("join/event/<int:event_id>",JoinEventView.as_view(),name="join_event"),
    path("myfeedback/<int:event_id>",FeedbackView.as_view(),name="myfeedback"),
    path("myevent/getfeedbacks/<int:event_id>",FeedbackListView.as_view(),name="list_feedbacks"),
    path("event_list",EventListAPIView.as_view(),name="list_event_public"),
    path("all_attendes/<int:id>",EventAttendeesAPIView.as_view(),name="list_attendees"),
    path("detail_event/<int:pk>",EventDetailView.as_view(),name="detail_event"),
    path('event_list_guest',EventWhoAttendeMe.as_view(),name="list_event_guest")
]

urlpatterns +=router.urls