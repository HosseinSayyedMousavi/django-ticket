from django.dispatch import receiver
from django.db.models.signals import post_save 
from .models import TicketMessage , TicketOptions
from datetime import datetime
@receiver(post_save, sender=TicketMessage)
def after_create_ticket_message(sender, instance, created, **kwargs):
    if created and instance.ticket:
        if instance.user and (instance.user.is_superuser or instance.user.is_staff):
            instance.ticket.status = TicketOptions.ANSWERED
            instance.ticket.seen_by_user = False
            instance.ticket.seen_by_admin =  True
            instance.viewed=datetime.now()
            instance.viewer=instance.user
            instance.save()
        else:
            instance.ticket.status = TicketOptions.PENDING
            instance.ticket.seen_by_user = True
            instance.ticket.ticketmessage_set.filter(viewed__isnull=True).exclude(user=instance.ticket.user.id).update(viewed=datetime.now(),viewer=instance.ticket.user.id)
    
        instance.ticket.save()
