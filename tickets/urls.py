from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminTicketViewSet,
    CustomerViewSet,
    AgentViewSet,
    FetchTicketsView,
    sell_ticket
)

# Admin urls for ticket app
router = DefaultRouter()
router.register(r'admin/tickets', AdminTicketViewSet, basename='admin-tickets')
router.register(r'admin/customers', CustomerViewSet, basename='admin-customers')
router.register(r'admin/agents', AgentViewSet, basename='admin-agents')

# Other urls including agent urls
urlpatterns = [
    path('', include(router.urls)),
    path('agent/fetch-tickets/', FetchTicketsView.as_view(), name='fetch-tickets'),
    path('agent/sell-ticket/<int:ticket_id>/', sell_ticket, name='sell-ticket'),
]
