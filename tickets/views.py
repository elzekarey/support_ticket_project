from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Ticket,Customer,User
from .serializers import TicketSerializer,CustomerSerializer,AgentSerializer
from .permissions import IsAdminUser, IsAgentUser


# Admin views for ticket app
class AdminTicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by('-created_at')
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

class AgentViewSet(viewsets.ModelViewSet):
    serializer_class = AgentSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return User.objects.filter(is_agent=True)

#Agent views for ticket app
class FetchTicketsView(APIView):
    permission_classes = [IsAgentUser]
    def get(self, request):
        agent = request.user
        assigned_tickets = Ticket.objects.filter(assigned_to=agent, status='assigned')
        #Checking number of assigned tickets
        if assigned_tickets.count() >= 15:
            return Response(TicketSerializer(assigned_tickets.order_by('created_at'), many=True).data)
        #If assigned tickets are less than 15
        tickets_needed = 15 - assigned_tickets.count()
        #Preventing racing conditions when concurrent requests act on the same table
        with transaction.atomic():
            unassigned_tickets = (Ticket.objects.select_for_update(skip_locked=True).filter(assigned_to__isnull=True, status='unassigned').order_by('created_at')[:tickets_needed])
            #Assigning more tickets to complete 15
            for ticket in unassigned_tickets:
                ticket.assigned_to = agent
                ticket.status = 'assigned'
                ticket.save()
        #Getting final assignedtickets (Should be 15)
        all_assigned = Ticket.objects.filter(assigned_to=agent, status='assigned').order_by('created_at')[:15]
        return Response(TicketSerializer(all_assigned, many=True).data)


#Selling Ticket
@api_view(['POST'])
@permission_classes([IsAgentUser])
def sell_ticket(request, ticket_id):
    agent = request.user
    try:
        ticket = Ticket.objects.get(id=ticket_id, assigned_to=agent, status='assigned')
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket was not found or was not assigned to you.'}, status=404)

    customer_data = request.data.get('customer')
    if not customer_data:
        return Response({'error': 'Customer data required.'}, status=400)

    # Create or get existing customer (you can customize deduplication logic)
    customer, _ = Customer.objects.get_or_create(email=customer_data['email'], defaults={'name': customer_data['name'],})
    ticket.customer = customer
    ticket.status = 'sold'
    ticket.save()
    return Response({'message': f'Ticket sold successfully to customer {customer_data["name"]}'}, status=200)
