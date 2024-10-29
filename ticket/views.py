from rest_framework.response import Response
from .models import Ticket, TicketMessage , TicketOptions
from django.contrib.auth import get_user_model
from rest_framework import generics ,permissions
from rest_framework.pagination import PageNumberPagination
from .serializers import   (TicketSerializer , CreateTicketSerializer , TicketDetailSerializer , AddMessageSerializer)
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from datetime import datetime
from django.utils.translation import gettext as _
User = get_user_model()


class ListPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100


class TicketAPIView(generics.ListAPIView):
    permission_classes =[permissions.IsAuthenticated]
    serializer_class = TicketSerializer
    pagination_class = ListPagination

    def get_queryset(self):
        queryset = Ticket.objects.filter(user = self.request.user.id,soft_delete=False).order_by('-id')
        return queryset
    
    @extend_schema(
        description=_("Get list of user's tickets"),
    )
    def get(self,*args,**kwargs):
        return super().get(*args,**kwargs)
        
    @extend_schema(
        responses={status.HTTP_201_CREATED: ''},
        description=_('Create a ticket from user'),
        examples=[
            OpenApiExample(
                name=_('body example'),
                value={
                            'title': 'string Maxlength=50 , Minlength=10',
                            'section': "'management' or 'finances' or 'technical'",
                            'priority': "'low' or 'medium' or 'high'",
                            'message': 'Maxlength=1000',
                            },
                request_only=True,
            )
        ]
    )
    def post(self,request):
        request.data['user']=request.user.id
        serializer = CreateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = {'message':serializer.validated_data['message'],
                   'user':serializer.validated_data['user']}
        serializer.validated_data.pop('message')
        ticket = Ticket.objects.create(**serializer.validated_data)
        ticket.ticketmessage_set.create(**message)
        return Response({'detail': _('Ticket successfully submitted.')},status=status.HTTP_201_CREATED)


class TicketDetailAPIView(generics.RetrieveAPIView):
    permission_classes =[permissions.IsAuthenticated]
    serializer_class = TicketDetailSerializer
    lookup_field = 'id' 

    def get_queryset(self):
        queryset = Ticket.objects.filter(user = self.request.user.id,soft_delete=False).order_by('-id')
        return queryset

    @extend_schema(
        description=_("Get a specific ticket detail with it's id and seen it"),
    )
    def get(self,*args,**kwargs):
        ticket = self.get_object()
        ticket.seen_by_user = True
        ticket.ticketmessage_set.filter(viewed__isnull=True,user=ticket.user.id).update(viewed=datetime.now(),viewer=ticket.user.id)
        ticket.save()
        return super().get(*args,**kwargs)
    
    @extend_schema(
        responses={status.HTTP_201_CREATED:_('Your message has been successfully submitted.')},
        description='Create a message on a ticket of user',
        examples=[
            OpenApiExample(
                name='body example',
                value={
                            'message': 'Maxlength=1000'
                            },
                request_only=True,
            )
        ]
    )
    def post(self,request,id):
        request.data['user']=request.user.id
        request.data['ticket']=id
        serializer = AddMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        TicketMessage.objects.create(**serializer.validated_data)

        return Response({'error': False, 'detail': _('Your message has been successfully submitted.')})

    @extend_schema(
        responses={status.HTTP_200_OK: _('Ticket closed.')},
        description=_('close a ticket'),
        request=None
    )
    def patch(self,request,id):
        ticket = self.get_object()
        ticket.status = TicketOptions.CLOSED
        ticket.save()
        return Response({'detail': _('Ticket closed.')})
