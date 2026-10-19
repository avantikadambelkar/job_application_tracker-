from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from .models import JobApplication, ApplicationTimeline

class JobApplicationModelTest(TestCase):
    def setUp(self):
        self.app = JobApplication.objects.create(
            company_name="Acme Corp",
            job_title="Senior Python Engineer",
            location="Remote",
            work_location_type="REMOTE",
            employment_type="FULL_TIME",
            salary_range="$130k - $160k",
            status="INTERVIEWING",
            priority="HIGH",
            application_date=date.today() - timedelta(days=5),
            tags="Python, Django, AWS, React",
            notes="Preparing for system design round"
        )

    def test_string_representation(self):
        self.assertEqual(str(self.app), "Senior Python Engineer at Acme Corp")

    def test_tag_list_property(self):
        self.assertEqual(self.app.tag_list, ["Python", "Django", "AWS", "React"])

    def test_days_since_applied(self):
        self.assertEqual(self.app.days_since_applied, 5)

    def test_status_badge_class(self):
        self.assertEqual(self.app.status_badge_class, "badge-interviewing")

    def test_timeline_relationship(self):
        timeline_event = ApplicationTimeline.objects.create(
            application=self.app,
            stage_title="Recruiter Screening",
            event_date=date.today(),
            notes="Great conversation"
        )
        self.assertEqual(self.app.timeline_events.count(), 1)
        self.assertEqual(self.app.timeline_events.first().stage_title, "Recruiter Screening")


class TrackerViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.app = JobApplication.objects.create(
            company_name="Netflix",
            job_title="Software Engineer",
            status="APPLIED",
            priority="HIGH",
            application_date=date.today()
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('tracker:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CareerPulse")
        self.assertContains(response, "Netflix")
        self.assertIn('stats', response.context)
        self.assertEqual(response.context['stats']['total_count'], 1)

    def test_kanban_view(self):
        response = self.client.get(reverse('tracker:kanban'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Application Pipeline Board")
        self.assertIn('columns', response.context)

    def test_analytics_view(self):
        response = self.client.get(reverse('tracker:analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Analytics & Insights")

    def test_application_detail_view(self):
        response = self.client.get(reverse('tracker:application_detail', kwargs={'pk': self.app.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Netflix")

    def test_application_create(self):
        data = {
            'company_name': 'Uber',
            'job_title': 'Backend Developer',
            'status': 'WISHLIST',
            'priority': 'MEDIUM',
            'work_location_type': 'HYBRID',
            'employment_type': 'FULL_TIME',
            'application_date': date.today(),
            'location': 'New York, NY',
            'salary_range': '$140k - $170k',
        }
        response = self.client.post(reverse('tracker:application_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(JobApplication.objects.filter(company_name='Uber').exists())

    def test_quick_status_update_ajax(self):
        response = self.client.post(
            reverse('tracker:quick_status_update', kwargs={'pk': self.app.pk}),
            {'status': 'INTERVIEWING'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.app.refresh_from_db()
        self.assertEqual(self.app.status, 'INTERVIEWING')

    def test_export_csv(self):
        response = self.client.get(reverse('tracker:export_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('Netflix', response.content.decode('utf-8'))

    def test_application_delete(self):
        response = self.client.post(reverse('tracker:application_delete', kwargs={'pk': self.app.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(JobApplication.objects.filter(pk=self.app.pk).exists())
