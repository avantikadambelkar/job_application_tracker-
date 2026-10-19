from django.contrib import admin
from .models import JobApplication, ApplicationTimeline

class ApplicationTimelineInline(admin.TabularInline):
    model = ApplicationTimeline
    extra = 1

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'job_title', 'status', 'work_location_type', 'priority', 'application_date', 'deadline_date')
    list_filter = ('status', 'work_location_type', 'priority', 'application_date')
    search_fields = ('company_name', 'job_title', 'tags', 'notes', 'recruiter_name')
    inlines = [ApplicationTimelineInline]
    date_hierarchy = 'application_date'

@admin.register(ApplicationTimeline)
class ApplicationTimelineAdmin(admin.ModelAdmin):
    list_display = ('application', 'stage_title', 'event_date', 'created_at')
    list_filter = ('event_date',)
    search_fields = ('stage_title', 'notes', 'application__company_name')
