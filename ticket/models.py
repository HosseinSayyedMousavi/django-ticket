import datetime
from datetime import timezone
from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

User = get_user_model()


class TicketOptions(Enum):
    # status
    PENDING = "pending"
    PENDING_LABEL = "Pending"
    ANSWERED = "answered"
    ANSWERED_LABEL = "Answered"
    CLOSED = "closed"
    CLOSED_LABEL = "Closed"

    # section
    MANAGEMENT = "management"
    MANAGEMENT_LABEL = "Management"
    FINANCES = "finances"
    FINANCES_LABEL = "Finances"
    SUPPORT = "support"
    SUPPORT_LABEL = "Support"

    # priority
    LOW = "low"
    LOW_LABEL = "Low"
    MEDIUM = "medium"
    MEDIUM_LABEL = "Medium"
    HIGH = "high"
    HIGH_LABEL = "High"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=[
        (TicketOptions.PENDING, _(TicketOptions.PENDING_LABEL)),
        (TicketOptions.ANSWERED, _(TicketOptions.ANSWERED_LABEL)),
        (TicketOptions.CLOSED, _(TicketOptions.CLOSED_LABEL))
    ], default=TicketOptions.PENDING)
    section = models.CharField(max_length=128, choices=[
        (TicketOptions.MANAGEMENT, _(TicketOptions.MANAGEMENT_LABEL)),
        (TicketOptions.FINANCES, _(TicketOptions.FINANCES_LABEL)),
        (TicketOptions.SUPPORT, _(TicketOptions.SUPPORT_LABEL))
    ], default=TicketOptions.SUPPORT)

    priority = models.CharField(max_length=128, choices=[
        (TicketOptions.LOW, _(TicketOptions.LOW_LABEL)),
        (TicketOptions.MEDIUM, _(TicketOptions.MEDIUM_LABEL)),
        (TicketOptions.HIGH_LABEL, _(TicketOptions.HIGH_LABEL))
    ], default=TicketOptions.LOW)

    seen_by_user = models.BooleanField(default=False, verbose_name=_("Seen by user"))
    seen_by_admin = models.BooleanField(default=False, verbose_name=_("Seen by admin"))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}:{self.title}"

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}:{self.message[:20]}"

    class Meta:
        verbose_name = _("Ticket Message")
        verbose_name_plural = _("Ticket Messages")
