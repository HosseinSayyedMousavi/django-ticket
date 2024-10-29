from django.urls import path
from . import views

app_name = "ticket"

urlpatterns = [
    path('ticket/', views.TicketAPIView.as_view()),
    path("ticket/<int:id>/",views.TicketDetailAPIView.as_view())
]
