from django.contrib import messages
from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.utils.translation import gettext as _

from .models import Ticket, TicketMessage
from .serializers import TicketSerializer, CreateTicketSerializer, AddMessageSerializer, SeeCloseTicketSerializer, \
    CreateTicketAPIViewSerializer, AddMessageAPIViewSerializer

User = get_user_model()


class CreateTicketAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateTicketAPIViewSerializer

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer = CreateTicketSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        message = {"message": serializer.validated_data["message"],
                   "user": serializer.validated_data["user"]}
        serializer.validated_data.pop("message")
        ticket = Ticket.objects.create(**serializer.validated_data)
        ticket.ticketmessage_set.create(**message)

        return Response(_("Ticket created successfully."), status=status.HTTP_201_CREATED)


class AddMessageAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AddMessageAPIViewSerializer

    def post(self, request):
        data = request.data
        data["user"] = request.user.id

        serializer = AddMessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        TicketMessage.objects.create(**serializer.validated_data)

        return Response({"error": 0, "message": _("Ticket message submitted successfully"), "type": "success"})


class CloseTicketAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SeeCloseTicketSerializer

    def patch(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.validated_data["ticket"]
        ticket.status = "closed"
        ticket.save()
        messages.add_message(request, messages.SUCCESS, "Ticket Closed")
        return Response({"message": _("Ticket Closed")})


class SeeTicketAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SeeCloseTicketSerializer

    def patch(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.validated_data["ticket"]
        ticket.seen_by_user = True
        ticket.save()

        return Response({"message": _("Ticket seen by user")})


class TicketListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.filter(user=self.request.user)
        return queryset
