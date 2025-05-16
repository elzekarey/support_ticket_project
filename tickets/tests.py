from django.test import TransactionTestCase
from rest_framework.test import APIClient
from .models import User, Ticket
from threading import Thread


class TicketConcurrencyTests(TransactionTestCase):
    reset_sequences = True
    def setUp(self):
        self.client = APIClient()
        self.agents = []

        for i in range(1, 6):
            username = f"agent{i}"
            password = f"agent{i}_pass"
            agent = User(username=username, is_agent=True, is_active=True)
            agent.set_password(password)
            agent.save()
            self.agents.append(agent)

        Ticket.objects.bulk_create([Ticket() for _ in range(100)])

        self.tokens = {}
        for agent in self.agents:
            res = self.client.post("/api/token/", {
                "username": agent.username,
                "password": f"{agent.username}_pass"
            })

            if res.status_code == 200:
                self.tokens[agent.username] = res.data["access"]
            else:
                print(f"[TOKEN FAIL] {agent.username}: {res.status_code} {res.content}")
                self.tokens[agent.username] = None

    def fetch_tickets(self, agent, results):
        client = APIClient()
        token = self.tokens.get(agent.username)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = client.get("/api/agent/fetch-tickets/")
        try:
            results[agent.username] = {
                'status': res.status_code,
                'count': len(res.data) if res.status_code == 200 else 0
            }
        except Exception as e:
            results[agent.username] = {'status': 500, 'count': 0, 'error': str(e)}

    def test_concurrent_assigning_unique_tickets(self):
        results = {}
        threads = [
            Thread(target=self.fetch_tickets, args=(agent, results))
            for agent in self.agents
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print("Thread results:", results)
        
        for r in results.values():
            self.assertEqual(r['status'], 200)
            self.assertLessEqual(r['count'], 15)

        all_tickets = Ticket.objects.exclude(assigned_to=None)
        self.assertEqual(all_tickets.count(), 75)
        self.assertEqual(
            all_tickets.values_list('id', flat=True).distinct().count(),
            all_tickets.count()
        )