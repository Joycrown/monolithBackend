from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, generics

from events.models import Event

from events.serializers import EventSerializer

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from events.serializers import EventAttendeesSerializer

from core.api.serializers import UserProfileSerializer
from events.models import Guest

from events.serializers import JoinSerailizer

from events.pagination import StandardResultsSetPagination


# Create your views here.
class EventListAPIView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'is_active','type')
    pagination_class = StandardResultsSetPagination

class EventAttendeesAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventAttendeesSerializer
    lookup_field = 'id'

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category','is_active','type')

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(owner=user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FeedbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        print(event.end_date)
        print(timezone.now())
        if event.end_date <timezone.now() :
            guest =get_object_or_404(Event,event=event, user=request.user)
            serializer = UserProfileSerializer(guest, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Event not finished yet !"}, status=status.HTTP_400_BAD_REQUEST)

class FeedbackListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, event_id):
        user=request.user
        event = get_object_or_404(Event,owner=user,id=event_id)
        if event is None:
            return  Response({"error":"Event not created by you. !"}, status=status.HTTP_400_BAD_REQUEST)
        feedbacks = Guest.objects.filter(event=event)
        serializer = UserProfileSerializer(feedbacks, many=True)
        return Response(serializer.data)

class EventWhoAttendeMe(ListAPIView):
    queryset=Event.objects.all()
    serializer_class=EventSerializer
    permission_classes=[AllowAny,]

    def get_queryset(self):
        user = self.request.user
        guest_events = Guest.objects.filter(user=user)
        event_ids = [guest.event.id for guest in guest_events]
        queryset = Event.objects.filter(id__in=event_ids)
        return queryset


class JoinEventView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if event.code_adhesion != request.data.get('code_adhesion'):
            return Response({"error": "Incorrect admission code."}, status=status.HTTP_400_BAD_REQUEST)
        guest, created = Guest.objects.get_or_create(event=event, user=request.user)
        return Response({"status": "Successfully joined event."}, status=status.HTTP_200_OK)
