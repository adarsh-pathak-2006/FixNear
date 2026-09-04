"""
Tests for the Celery dispatch_repair_request task and its signal trigger.

CELERY_TASK_ALWAYS_EAGER = True (set when DEBUG=True in settings) means
tasks execute synchronously inside the test process — no broker or worker needed.
"""

from django.test import TestCase, TransactionTestCase, override_settings
from django.contrib.auth import get_user_model
from authentication.models import CustomerProfile, TechnicianProfile
from customer.models import RepairRequest
from technician.models import SentRequest
from fixnear.tasks import dispatch_repair_request

User = get_user_model()

EAGER_CELERY = {
    'CELERY_TASK_ALWAYS_EAGER': True,
    'CELERY_TASK_EAGER_PROPAGATES': True,
}


def make_user(username, role, skill=None):
    user = User.objects.create_user(
        username=username,
        email=f'{username}@test.com',
        mobile_no=f'900000{User.objects.count():04d}',
        password='testpass123',
        role=role,
    )
    if role == 'TECHNICIAN' and skill:
        TechnicianProfile.objects.filter(user=user).update(skill=skill, is_available=True)
    return user


# ─── Task unit tests ──────────────────────────────────────────────────────────

@override_settings(**EAGER_CELERY)
class DispatchTaskTests(TestCase):

    def setUp(self):
        self.customer_user = make_user('cust1', 'CUSTOMER')
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)

        self.tech1 = make_user('tech1', 'TECHNICIAN', skill='LAPTOP_REPAIR')
        self.tech2 = make_user('tech2', 'TECHNICIAN', skill='LAPTOP_REPAIR')
        self.tech3 = make_user('tech3', 'TECHNICIAN', skill='PLUMBER')

    def _make_request(self, skill):
        return RepairRequest.objects.create(
            user=self.customer_profile,
            skills_required=skill,
            requirement='Test requirement',
        )

    def test_task_creates_sent_requests_for_matching_technicians(self):
        repair = self._make_request('LAPTOP_REPAIR')
        SentRequest.objects.all().delete()

        dispatch_repair_request(repair.pk)

        sent = SentRequest.objects.filter(request=repair)
        self.assertEqual(sent.count(), 2)
        technician_users = set(s.technician.user.username for s in sent)
        self.assertIn('tech1', technician_users)
        self.assertIn('tech2', technician_users)

    def test_task_does_not_dispatch_to_wrong_skill(self):
        repair = self._make_request('LAPTOP_REPAIR')
        SentRequest.objects.all().delete()

        dispatch_repair_request(repair.pk)

        plumber_profile = TechnicianProfile.objects.get(user=self.tech3)
        self.assertFalse(
            SentRequest.objects.filter(request=repair, technician=plumber_profile).exists()
        )

    def test_task_skips_unavailable_technicians(self):
        TechnicianProfile.objects.filter(user=self.tech2).update(is_available=False)
        repair = self._make_request('LAPTOP_REPAIR')
        SentRequest.objects.all().delete()

        dispatch_repair_request(repair.pk)

        sent = SentRequest.objects.filter(request=repair)
        self.assertEqual(sent.count(), 1)
        self.assertEqual(sent.first().technician.user.username, 'tech1')

    def test_task_is_idempotent_on_retry(self):
        repair = self._make_request('LAPTOP_REPAIR')
        SentRequest.objects.all().delete()

        dispatch_repair_request(repair.pk)
        dispatch_repair_request(repair.pk)

        sent = SentRequest.objects.filter(request=repair)
        self.assertEqual(sent.count(), 2, 'Duplicate SentRequests must not be created on retry')

    def test_task_is_noop_for_nonexistent_repair_request(self):
        dispatch_repair_request(999999)
        self.assertEqual(SentRequest.objects.count(), 0)

    def test_task_creates_no_sent_requests_when_no_technicians_match(self):
        repair = self._make_request('ELECTRICIAN')
        SentRequest.objects.all().delete()

        dispatch_repair_request(repair.pk)

        self.assertEqual(SentRequest.objects.filter(request=repair).count(), 0)


# ─── Signal integration tests ─────────────────────────────────────────────────

@override_settings(**EAGER_CELERY)
class SignalDispatchIntegrationTests(TransactionTestCase):

    def setUp(self):
        self.customer_user = make_user('cust2', 'CUSTOMER')
        self.customer_profile = CustomerProfile.objects.get(user=self.customer_user)

        self.tech_a = make_user('tech_a', 'TECHNICIAN', skill='ELECTRICIAN')
        self.tech_b = make_user('tech_b', 'TECHNICIAN', skill='ELECTRICIAN')

    def test_creating_repair_request_auto_dispatches_to_technicians(self):
        RepairRequest.objects.create(
            user=self.customer_profile,
            skills_required='ELECTRICIAN',
            requirement='Power outlet not working',
        )
        self.assertEqual(SentRequest.objects.count(), 2)

    def test_no_dispatch_if_no_available_technicians(self):
        TechnicianProfile.objects.filter(
            user__in=[self.tech_a, self.tech_b]
        ).update(is_available=False)

        RepairRequest.objects.create(
            user=self.customer_profile,
            skills_required='ELECTRICIAN',
            requirement='Power outlet not working',
        )
        self.assertEqual(SentRequest.objects.count(), 0)

    def test_signal_does_not_dispatch_on_repair_request_update(self):
        repair = RepairRequest.objects.create(
            user=self.customer_profile,
            skills_required='ELECTRICIAN',
            requirement='Initial requirement',
        )
        count_after_create = SentRequest.objects.count()

        repair.requirement = 'Updated requirement'
        repair.save()

        self.assertEqual(
            SentRequest.objects.count(),
            count_after_create,
            'Updating an existing RepairRequest must not trigger re-dispatch',
        )


# ─── Profile auto-creation signal tests ──────────────────────────────────────

class ProfileAutoCreationTests(TestCase):

    def test_customer_profile_created_on_registration(self):
        user = make_user('new_cust', 'CUSTOMER')
        self.assertTrue(CustomerProfile.objects.filter(user=user).exists())
        self.assertFalse(TechnicianProfile.objects.filter(user=user).exists())

    def test_technician_profile_created_on_registration(self):
        user = make_user('new_tech', 'TECHNICIAN')
        self.assertTrue(TechnicianProfile.objects.filter(user=user).exists())
        self.assertFalse(CustomerProfile.objects.filter(user=user).exists())

    def test_admin_gets_no_profile(self):
        user = User.objects.create_superuser(
            username='admin_user',
            email='admin@test.com',
            mobile_no='9000000001',
            password='adminpass',
            role='ADMIN',
        )
        self.assertFalse(CustomerProfile.objects.filter(user=user).exists())
        self.assertFalse(TechnicianProfile.objects.filter(user=user).exists())
