from django.urls import path
from . import views

app_name = "ticket"

urlpatterns = [
    path('', views.TicketAPIView.as_view()),
    path('<int:id>/',views.TicketDetailAPIView.as_view())
]
