import csv
import json
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import JobApplication, ApplicationTimeline
from .forms import JobApplicationForm, ApplicationTimelineForm

def get_stats_context():
    """Helper to compute aggregate metrics across all applications"""
    total = JobApplication.objects.count()
    applied = JobApplication.objects.filter(status='APPLIED').count()
    interviewing = JobApplication.objects.filter(status='INTERVIEWING').count()
    offered = JobApplication.objects.filter(status='OFFERED').count()
    rejected = JobApplication.objects.filter(status='REJECTED').count()
    wishlist = JobApplication.objects.filter(status='WISHLIST').count()
    accepted = JobApplication.objects.filter(status='ACCEPTED').count()
    
    # Calculate response rate: (interviewing + offered + accepted + rejected) / (total - wishlist)
    active_considered = total - wishlist
    if active_considered > 0:
        responded = interviewing + offered + accepted + rejected
        response_rate = round((responded / active_considered) * 100, 1)
    else:
        response_rate = 0.0

    today = date.today()
    upcoming_followups = JobApplication.objects.filter(
        follow_up_date__gte=today
    ).order_by('follow_up_date')[:5]

    return {
        'total_count': total,
        'applied_count': applied,
        'interviewing_count': interviewing,
        'offered_count': offered,
        'rejected_count': rejected,
        'wishlist_count': wishlist,
        'accepted_count': accepted,
        'response_rate': response_rate,
        'upcoming_followups': upcoming_followups,
    }

def dashboard_view(request):
    applications = JobApplication.objects.all()
    stats = get_stats_context()
    
    # Filtering
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    work_type_filter = request.GET.get('work_type', '').strip()
    priority_filter = request.GET.get('priority', '').strip()
    sort_by = request.GET.get('sort', '-application_date').strip()

    if query:
        applications = applications.filter(
            Q(company_name__icontains=query) |
            Q(job_title__icontains=query) |
            Q(tags__icontains=query) |
            Q(location__icontains=query) |
            Q(recruiter_name__icontains=query)
        )

    if status_filter:
        applications = applications.filter(status=status_filter)

    if work_type_filter:
        applications = applications.filter(work_location_type=work_type_filter)

    if priority_filter:
        applications = applications.filter(priority=priority_filter)

    valid_sorts = {
        'newest': '-application_date',
        'oldest': 'application_date',
        'company': 'company_name',
        'priority': '-priority',
        'deadline': 'deadline_date',
    }
    sort_field = valid_sorts.get(sort_by, '-application_date')
    applications = applications.order_by(sort_field, '-created_at')

    # Modal quick form
    quick_form = JobApplicationForm()

    context = {
        'applications': applications,
        'stats': stats,
        'query': query,
        'status_filter': status_filter,
        'work_type_filter': work_type_filter,
        'priority_filter': priority_filter,
        'sort_by': sort_by,
        'quick_form': quick_form,
        'status_choices': JobApplication.STATUS_CHOICES,
        'work_type_choices': JobApplication.WORK_TYPE_CHOICES,
        'priority_choices': JobApplication.PRIORITY_CHOICES,
        'active_tab': 'dashboard',
    }
    return render(request, 'tracker/dashboard.html', context)

def kanban_view(request):
    stats = get_stats_context()
    query = request.GET.get('q', '').strip()
    
    queryset = JobApplication.objects.all()
    if query:
        queryset = queryset.filter(
            Q(company_name__icontains=query) |
            Q(job_title__icontains=query) |
            Q(tags__icontains=query)
        )

    columns = [
        {'status': 'WISHLIST', 'label': 'Wishlist / Saved', 'badge': 'badge-wishlist', 'icon': 'bi-bookmark-star', 'items': queryset.filter(status='WISHLIST')},
        {'status': 'APPLIED', 'label': 'Applied', 'badge': 'badge-applied', 'icon': 'bi-send-check', 'items': queryset.filter(status='APPLIED')},
        {'status': 'INTERVIEWING', 'label': 'Interviewing', 'badge': 'badge-interviewing', 'icon': 'bi-camera-video', 'items': queryset.filter(status='INTERVIEWING')},
        {'status': 'OFFERED', 'label': 'Offers', 'badge': 'badge-offered', 'icon': 'bi-trophy-fill', 'items': queryset.filter(status='OFFERED')},
        {'status': 'REJECTED', 'label': 'Rejected', 'badge': 'badge-rejected', 'icon': 'bi-x-circle', 'items': queryset.filter(status='REJECTED')},
    ]

    quick_form = JobApplicationForm()

    context = {
        'stats': stats,
        'columns': columns,
        'query': query,
        'quick_form': quick_form,
        'status_choices': JobApplication.STATUS_CHOICES,
        'active_tab': 'kanban',
    }
    return render(request, 'tracker/kanban.html', context)

def application_detail_view(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    timeline_form = ApplicationTimelineForm()
    timeline_events = application.timeline_events.all()

    context = {
        'application': application,
        'timeline_events': timeline_events,
        'timeline_form': timeline_form,
        'status_choices': JobApplication.STATUS_CHOICES,
    }
    return render(request, 'tracker/application_detail.html', context)

def application_create_view(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            messages.success(request, f"Successfully tracked application for {application.job_title} at {application.company_name}!")
            return redirect('tracker:application_detail', pk=application.pk)
        else:
            messages.error(request, "Please check the form inputs for errors.")
    else:
        form = JobApplicationForm()

    context = {
        'form': form,
        'title': 'Add New Job Application',
        'button_text': 'Track Application',
    }
    return render(request, 'tracker/application_form.html', context)

def application_update_view(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated application details for {application.company_name}.")
            return redirect('tracker:application_detail', pk=application.pk)
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = JobApplicationForm(instance=application)

    context = {
        'form': form,
        'application': application,
        'title': f'Edit Application — {application.company_name}',
        'button_text': 'Save Changes',
    }
    return render(request, 'tracker/application_form.html', context)

def application_delete_view(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    company = application.company_name
    title = application.job_title
    
    if request.method == 'POST':
        application.delete()
        messages.success(request, f"Application for {title} at {company} was removed.")
        return redirect('tracker:dashboard')

    return render(request, 'tracker/application_confirm_delete.html', {'application': application})

def quick_status_update_view(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    new_status = request.POST.get('status') or request.GET.get('status')
    
    valid_statuses = [s[0] for s in JobApplication.STATUS_CHOICES]
    if new_status in valid_statuses:
        old_status = application.status
        application.status = new_status
        application.save()

        # Automatically log a timeline milestone if moving to Interviewing or Offered
        if new_status == 'INTERVIEWING' and old_status != 'INTERVIEWING':
            ApplicationTimeline.objects.create(
                application=application,
                stage_title="Advanced to Interview Stage",
                event_date=date.today(),
                notes=f"Status transitioned from {old_status} to INTERVIEWING."
            )
        elif new_status == 'OFFERED' and old_status != 'OFFERED':
            ApplicationTimeline.objects.create(
                application=application,
                stage_title="Job Offer Received! 🎉",
                event_date=date.today(),
                notes=f"Received official job offer."
            )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'success': True,
                'status': new_status,
                'status_label': application.get_status_display(),
                'status_badge_class': application.status_badge_class,
                'message': f"Status updated to {application.get_status_display()}"
            })
            
        messages.success(request, f"Updated {application.company_name} status to {application.get_status_display()}.")
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
        messages.error(request, "Invalid status choice selected.")

    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or 'tracker:dashboard'
    return redirect(next_url)

def add_timeline_event_view(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        form = ApplicationTimelineForm(request.POST)
        if form.is_valid():
            timeline_event = form.save(commit=False)
            timeline_event.application = application
            timeline_event.save()
            messages.success(request, f"Added timeline event: {timeline_event.stage_title}")
        else:
            messages.error(request, "Could not add timeline event. Please check inputs.")
    return redirect('tracker:application_detail', pk=pk)

def analytics_view(request):
    stats = get_stats_context()
    applications = JobApplication.objects.all()

    # Status distribution
    status_counts = {}
    for code, label in JobApplication.STATUS_CHOICES:
        count = applications.filter(status=code).count()
        if count > 0:
            status_counts[label] = count

    # Work location distribution
    work_type_counts = {}
    for code, label in JobApplication.WORK_TYPE_CHOICES:
        work_type_counts[label] = applications.filter(work_location_type=code).count()

    # Priority distribution
    priority_counts = {}
    for code, label in JobApplication.PRIORITY_CHOICES:
        priority_counts[label] = applications.filter(priority=code).count()

    # Popular tags extraction
    tag_counter = {}
    for app in applications:
        for t in app.tag_list:
            tag_counter[t] = tag_counter.get(t, 0) + 1
    sorted_tags = sorted(tag_counter.items(), key=lambda x: x[1], reverse=True)[:8]

    context = {
        'stats': stats,
        'status_counts_json': json.dumps(status_counts),
        'work_type_counts_json': json.dumps(work_type_counts),
        'priority_counts_json': json.dumps(priority_counts),
        'top_tags': sorted_tags,
        'active_tab': 'analytics',
    }
    return render(request, 'tracker/analytics.html', context)

def export_csv_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="job_applications_{date.today()}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Company', 'Job Title', 'Status', 'Work Type', 'Location',
        'Salary Range', 'Priority', 'Application Date', 'Deadline',
        'Recruiter Name', 'Recruiter Email', 'Tags', 'Resume Used'
    ])

    for app in JobApplication.objects.all():
        writer.writerow([
            app.company_name,
            app.job_title,
            app.get_status_display(),
            app.get_work_location_type_display(),
            app.location,
            app.salary_range,
            app.get_priority_display(),
            app.application_date,
            app.deadline_date or '',
            app.recruiter_name,
            app.recruiter_email,
            app.tags,
            app.resume_version,
        ])

    return response

def seed_demo_data_view(request):
    """Seed high quality realistic sample data for showcase and resume demo"""
    from datetime import timedelta
    today = date.today()

    demo_data = [
        {
            'company_name': 'Google',
            'job_title': 'Software Engineer III - Cloud Platform',
            'job_url': 'https://careers.google.com/jobs/results/10982',
            'location': 'Mountain View, CA / Hybrid',
            'work_location_type': 'HYBRID',
            'employment_type': 'FULL_TIME',
            'salary_range': '$165,000 - $195,000',
            'status': 'INTERVIEWING',
            'priority': 'HIGH',
            'application_date': today - timedelta(days=14),
            'follow_up_date': today + timedelta(days=3),
            'recruiter_name': 'Jessica Sterling',
            'recruiter_email': 'jsterling@google.com',
            'recruiter_linkedin': 'https://linkedin.com/in/jessica-sterling-recruiter',
            'tags': 'Python, Distributed Systems, Go, Kubernetes',
            'resume_version': 'Alex_SDE_Backend_2026.pdf',
            'job_description': 'Design, build, and deploy high-throughput microservices in Go and Python on Google Cloud Platform. Collaborate with cross-functional teams to improve latency and reliability.',
            'notes': 'Completed recruiter screen and online coding assessment. Technical system design round scheduled for next Thursday.',
            'timeline': [
                ("Application Submitted", today - timedelta(days=14), "Submitted via Google Careers portal."),
                ("Recruiter Screening", today - timedelta(days=9), "30-min call with Jessica. Discussed distributed systems background."),
                ("Technical Assessment Passed", today - timedelta(days=4), "Passed 2 algorithmic challenges with 100% test coverage."),
            ]
        },
        {
            'company_name': 'Stripe',
            'job_title': 'Full Stack Engineer - Billing & Subscriptions',
            'job_url': 'https://stripe.com/jobs/listing/45021',
            'location': 'San Francisco, CA / Remote',
            'work_location_type': 'REMOTE',
            'employment_type': 'FULL_TIME',
            'salary_range': '$175,000 - $210,000 + Equity',
            'status': 'OFFERED',
            'priority': 'HIGH',
            'application_date': today - timedelta(days=28),
            'follow_up_date': today + timedelta(days=2),
            'recruiter_name': 'David Chen',
            'recruiter_email': 'dchen@stripe.com',
            'recruiter_linkedin': 'https://linkedin.com/in/davidchen-stripe',
            'tags': 'Ruby, Python, React, PostgreSQL, Stripe API',
            'resume_version': 'Alex_FullStack_2026.pdf',
            'job_description': 'Architect user-facing payment flows and subscription life-cycle tools serving millions of global businesses.',
            'notes': 'Formal offer letter received! Base: $185k, $70k equity over 4 years. Reviewing counter-offer strategy.',
            'timeline': [
                ("Application Submitted", today - timedelta(days=28), "Applied with employee referral."),
                ("First Round Video Interview", today - timedelta(days=21), "Live pair programming session building an idempotent webhook receiver."),
                ("Virtual Onsite Completed", today - timedelta(days=10), "4 rounds: Architecture, Product Sense, Coding, Culture."),
                ("Job Offer Received! 🎉", today - timedelta(days=2), "Received written offer letter."),
            ]
        },
        {
            'company_name': 'Spotify',
            'job_title': 'Backend Developer - Discovery & Recommendations',
            'job_url': 'https://spotify.com/jobs/backend-engineer-discovery',
            'location': 'New York, NY / Hybrid',
            'work_location_type': 'HYBRID',
            'employment_type': 'FULL_TIME',
            'salary_range': '$150,000 - $175,000',
            'status': 'INTERVIEWING',
            'priority': 'HIGH',
            'application_date': today - timedelta(days=18),
            'follow_up_date': today + timedelta(days=5),
            'recruiter_name': 'Elena Rostova',
            'recruiter_email': 'erostova@spotify.com',
            'tags': 'Python, Django, FastAPI, Kafka, Docker',
            'resume_version': 'Alex_SDE_Backend_2026.pdf',
            'job_description': 'Build high scale recommendation ingestion pipelines using Python, Kafka, and Redis.',
            'notes': 'Round 2 coding interview next Monday. Brush up on caching strategies and Kafka consumer groups.',
            'timeline': [
                ("Applied", today - timedelta(days=18), "Applied via LinkedIn easy apply."),
                ("Screening Call", today - timedelta(days=11), "Discussed music streaming passion and Python async experience."),
            ]
        },
        {
            'company_name': 'Airbnb',
            'job_title': 'Senior Frontend / UI Engineer',
            'job_url': 'https://careers.airbnb.com/positions/39102',
            'location': 'San Francisco, CA (Remote)',
            'work_location_type': 'REMOTE',
            'employment_type': 'FULL_TIME',
            'salary_range': '$160,000 - $185,000',
            'status': 'APPLIED',
            'priority': 'MEDIUM',
            'application_date': today - timedelta(days=6),
            'deadline_date': today + timedelta(days=20),
            'follow_up_date': today + timedelta(days=8),
            'tags': 'React, TypeScript, Design Systems, CSS',
            'resume_version': 'Alex_Frontend_UI_2026.pdf',
            'job_description': 'Craft world-class booking experiences and enhance Airbnb design system components.',
            'notes': 'Referred by college alumni. Application under hiring manager review.',
            'timeline': [
                ("Application Submitted", today - timedelta(days=6), "Submitted with internal referral."),
            ]
        },
        {
            'company_name': 'Datadog',
            'job_title': 'Software Engineer - Infrastructure Monitoring',
            'job_url': 'https://datadoghq.com/careers/infra-eng',
            'location': 'Boston, MA / Remote',
            'work_location_type': 'REMOTE',
            'employment_type': 'FULL_TIME',
            'salary_range': '$140,000 - $165,000',
            'status': 'APPLIED',
            'priority': 'MEDIUM',
            'application_date': today - timedelta(days=4),
            'tags': 'Python, Linux, Prometheus, Grafana, AWS',
            'resume_version': 'Alex_SDE_Backend_2026.pdf',
            'job_description': 'Telemetry metrics aggregation and real-time dashboard instrumentation backend.',
            'notes': 'Recruiter viewed application on LinkedIn.',
            'timeline': []
        },
        {
            'company_name': 'Linear',
            'job_title': 'Product Engineer - Workflows & Integrations',
            'job_url': 'https://linear.app/careers/product-engineer',
            'location': 'Remote (Global)',
            'work_location_type': 'REMOTE',
            'employment_type': 'FULL_TIME',
            'salary_range': '$155,000 - $185,000',
            'status': 'WISHLIST',
            'priority': 'HIGH',
            'application_date': today,
            'tags': 'TypeScript, GraphQL, Node.js, UI/UX',
            'resume_version': 'Alex_FullStack_2026.pdf',
            'job_description': 'Build lightning-fast issue tracking workflows and keyboard-first developer interfaces.',
            'notes': 'Polishing portfolio project before submitting tailored cover letter.',
            'timeline': []
        },
        {
            'company_name': 'Amazon AWS',
            'job_title': 'Software Development Engineer II',
            'job_url': 'https://amazon.jobs/en/jobs/2199042',
            'location': 'Seattle, WA / Hybrid',
            'work_location_type': 'HYBRID',
            'employment_type': 'FULL_TIME',
            'salary_range': '$160,000 - $185,000',
            'status': 'REJECTED',
            'priority': 'LOW',
            'application_date': today - timedelta(days=35),
            'tags': 'Java, AWS, DynamoDB, Systems',
            'resume_version': 'Alex_General_2026.pdf',
            'job_description': 'AWS Lambda execution runtime backend engineering.',
            'notes': 'Position filled internally. Encouraged to reapply for team in 6 months.',
            'timeline': [
                ("Applied", today - timedelta(days=35), "Direct submission."),
                ("Automated Update", today - timedelta(days=12), "Team moved forward with internal candidate."),
            ]
        },
    ]

    count_created = 0
    for item in demo_data:
        timeline_items = item.pop('timeline', [])
        app, created = JobApplication.objects.get_or_create(
            company_name=item['company_name'],
            job_title=item['job_title'],
            defaults=item
        )
        if created:
            count_created += 1
            for title, event_dt, notes in timeline_items:
                ApplicationTimeline.objects.create(
                    application=app,
                    stage_title=title,
                    event_date=event_dt,
                    notes=notes
                )

    messages.success(request, f"Loaded {count_created} demo job applications with timeline history!")
    return redirect('tracker:dashboard')
