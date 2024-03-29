import datetime
from datetime import timezone

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[
        ("pending", "pending"),
        ("answered", "answered"),
        ("closed", "closed")
    ], default="pending")

    title = models.CharField(max_length=255)
    section = models.CharField(max_length=128, choices=[
        ("management", "management"),
        ("finances", "finances"),
        ("support", "support")
    ])
    priority = models.CharField(max_length=128, choices=[
        ("low", "low"),
        ("medium", "medium"),
        ("high", "high")
    ], default="low")

    seen_by_user = models.BooleanField(default=False)
    seen_by_admin = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):

        if self.pk:
            last_message = self.ticketmessage_set.order_by("-id").first()
        else:
            last_message = None
        if self.status != "closed" and last_message:
            if last_message.user and last_message.user.is_superuser:
                self.status = "answered"
                self.seen_by_admin = True
                now = datetime.datetime.now(timezone.utc)
                if (now - last_message.created).seconds < 5:
                    self.seen_by_user = False
            else:
                self.status = "pending"

        super(Ticket, self).save(*args, **kwargs)


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=TicketMessage)
def aftercreate(sender, instance, created, **kwargs):
    if created and instance.ticket and instance.ticket.status != "closed":
        if instance.user and (instance.user.is_superuser or instance.user.is_staff):
            instance.ticket.status = "answered"
        else:
            instance.ticket.status = "pending"

    instance.ticket.save()
