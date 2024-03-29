from django.contrib.auth import get_user_model

from .models import Ticket

User = get_user_model()


def get_pending_tickets(request):
    return {
        "pending_tickets": Ticket.objects.filter(status="pending").count(),
    }
