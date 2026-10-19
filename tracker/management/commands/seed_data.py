from django.core.management.base import BaseCommand
from tracker.views import seed_demo_data_view
from tracker.models import JobApplication
from django.test import RequestFactory

class Command(BaseCommand):
    help = 'Seeds sample realistic job application data for testing and portfolio demos'

    def handle(self, *args, **options):
        initial_count = JobApplication.objects.count()
        factory = RequestFactory()
        request = factory.get('/seed-demo/')
        # set session/messages mocks if needed
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', {})
        setattr(request, '_messages', FallbackStorage(request))

        seed_demo_data_view(request)
        final_count = JobApplication.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded! Total applications in database: {final_count} (added {final_count - initial_count})'))
