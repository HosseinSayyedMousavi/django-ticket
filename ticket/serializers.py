import difflib

from django.utils.translation import gettext as _
from rest_framework import serializers, exceptions

from .models import Ticket, TicketMessage


class CreateTicketSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=True)

    class Meta:
        model = Ticket
        fields = ("user", "status", "title", "section", "priority", "seen_by_admin", "seen_by_user", "message")

    def validate(self, attrs):
        valid = super().validate(attrs)
        valid["status"] = "pending"
        valid["seen_by_user"] = True
        valid["seen_by_admin"] = False
        if not attrs.get("priority"):
            valid["priority"] = "کم"
        if not attrs.get("section"):
            valid["section"] = _("support")
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
        valid = super().validate(attrs)
        ticket = attrs.get("ticket")

        if ticket.user.id != attrs.get("user").id:
            try:  # suspend user :
                attrs.get("user").is_active = False
                attrs.get("user").save()
            except:
                pass
            raise exceptions.ValidationError({"message": "این تیکت متعلق به شما نیست"})

        if not ticket or ticket.status == "closed":
            raise exceptions.ValidationError({"message": "تیکت بسته شده است"})
        if attrs.get("message", None):
            if any([difflib.SequenceMatcher(None, attrs.get("message"), x.message).ratio() > 0.85 for x in
                    TicketMessage.objects.filter(ticket=ticket)]):
                raise exceptions.ValidationError(
                    {"message": "متنی با تشابه تقریبی 85 درصد و بالاتر ، قبلا ارسال شده است."})

        return valid


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
