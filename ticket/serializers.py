import difflib

from django.utils.translation import gettext as _
from rest_framework import serializers, exceptions

from .models import Ticket, TicketMessage, TicketOptions


class CreateTicketSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=True)

    class Meta:
        model = Ticket
        fields = ("user", "status", "title", "section", "priority", "seen_by_admin", "seen_by_user", "message")

    def validate(self, attrs):
        valid = super().validate(attrs)
        valid["seen_by_user"] = True
        if not attrs.get("priority"):
            valid["priority"] = TicketOptions.LOW
        if not attrs.get("section"):
            valid["section"] = TicketOptions.SUPPORT
        return valid


class CreateTicketAPIViewSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=True)

    class Meta:
        model = Ticket
        fields = ("title", "section", "priority", "message")


class AddMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = ("user", "ticket", "message")

    def validate(self, attrs):
        ticket = attrs.get("ticket")
        user = attrs.get("user")
        message = attrs.get("message", None)

        if ticket.user.id != user.id:
            raise exceptions.PermissionDenied()

        if ticket.status == TicketOptions.CLOSED:
            raise exceptions.ValidationError(_("Ticket has been closed."))

        if any([difflib.SequenceMatcher(None, message, x.message).ratio() > 0.85 for x in
                TicketMessage.objects.filter(ticket=ticket)]):
            raise exceptions.ValidationError(
                {"message": _("Message with similarity of 85% has already been sent.")})

        return attrs


class AddMessageAPIViewSerializer(AddMessageSerializer):
    class Meta(AddMessageSerializer.Meta):
        fields = ("ticket", "message")


class SeeCloseTicketSerializer(serializers.ModelSerializer):
    class Meta(AddMessageSerializer.Meta):
        fields = ("ticket",)


class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    ticketmessage_set = TicketMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"
