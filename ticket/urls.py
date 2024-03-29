from django.urls import path
from . import views

app_name = "ticket"

urlpatterns = [
    path("create_ticket/", views.CreateTicketAPIView.as_view()),
    path("add_message/", views.AddMessageAPIView.as_view()),
    path("close/", views.CloseTicketAPIView.as_view()),
    path("seen/", views.SeeTicketAPIView.as_view()),
    path("get_my_tickets/", views.TicketListAPIView.as_view())
]
