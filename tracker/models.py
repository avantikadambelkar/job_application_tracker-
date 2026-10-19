from django.db import models
from django.utils import timezone
from datetime import date

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('WISHLIST', 'Wishlist / Saved'),
        ('APPLIED', 'Applied'),
        ('INTERVIEWING', 'Interviewing'),
        ('OFFERED', 'Offered'),
        ('REJECTED', 'Rejected'),
        ('ACCEPTED', 'Accepted'),
        ('WITHDRAWN', 'Withdrawn'),
    ]

    WORK_TYPE_CHOICES = [
        ('REMOTE', 'Remote'),
        ('HYBRID', 'Hybrid'),
        ('ONSITE', 'On-site'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('FULL_TIME', 'Full-time'),
        ('PART_TIME', 'Part-time'),
        ('INTERNSHIP', 'Internship'),
        ('CONTRACT', 'Contract'),
    ]

    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    company_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=200)
    job_url = models.URLField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, default='Remote')
    work_location_type = models.CharField(max_length=20, choices=WORK_TYPE_CHOICES, default='REMOTE')
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='FULL_TIME')
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g. $120,000 - $150,000 or ₹18-24 LPA")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    application_date = models.DateField(default=timezone.now)
    deadline_date = models.DateField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    
    recruiter_name = models.CharField(max_length=120, blank=True)
    recruiter_email = models.EmailField(blank=True)
    recruiter_linkedin = models.URLField(max_length=500, blank=True)
    
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated e.g. Python, Django, React, AI")
    resume_version = models.CharField(max_length=120, blank=True, help_text="e.g. Resume_SDE_2026.pdf")
    job_description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-application_date', '-created_at']

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

    @property
    def tag_list(self):
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    @property
    def days_since_applied(self):
        if self.application_date:
            return (date.today() - self.application_date).days
        return 0

    @property
    def status_badge_class(self):
        badges = {
            'WISHLIST': 'badge-wishlist',
            'APPLIED': 'badge-applied',
            'INTERVIEWING': 'badge-interviewing',
            'OFFERED': 'badge-offered',
            'REJECTED': 'badge-rejected',
            'ACCEPTED': 'badge-accepted',
            'WITHDRAWN': 'badge-withdrawn',
        }
        return badges.get(self.status, 'badge-secondary')

    @property
    def status_icon(self):
        icons = {
            'WISHLIST': 'bi-bookmark-star',
            'APPLIED': 'bi-send-check',
            'INTERVIEWING': 'bi-camera-video',
            'OFFERED': 'bi-trophy-fill',
            'REJECTED': 'bi-x-circle',
            'ACCEPTED': 'bi-check2-circle',
            'WITHDRAWN': 'bi-arrow-counterclockwise',
        }
        return icons.get(self.status, 'bi-record-circle')

    @property
    def priority_badge_class(self):
        badges = {
            'HIGH': 'priority-high',
            'MEDIUM': 'priority-medium',
            'LOW': 'priority-low',
        }
        return badges.get(self.priority, 'priority-medium')


class ApplicationTimeline(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='timeline_events')
    stage_title = models.CharField(max_length=150)
    event_date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-event_date', '-created_at']

    def __str__(self):
        return f"{self.stage_title} on {self.event_date} for {self.application.company_name}"
