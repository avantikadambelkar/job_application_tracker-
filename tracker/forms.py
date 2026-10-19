from django import forms
from .models import JobApplication, ApplicationTimeline

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'company_name',
            'job_title',
            'job_url',
            'location',
            'work_location_type',
            'employment_type',
            'salary_range',
            'status',
            'priority',
            'application_date',
            'deadline_date',
            'follow_up_date',
            'recruiter_name',
            'recruiter_email',
            'recruiter_linkedin',
            'tags',
            'resume_version',
            'job_description',
            'notes',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Google, Stripe, Microsoft',
                'required': True,
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Full Stack Python / Django Developer',
                'required': True,
            }),
            'job_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://careers.company.com/job/12345',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. San Francisco, CA or Remote',
            }),
            'work_location_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'employment_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'salary_range': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. $120,000 - $145,000 or ₹18-25 LPA',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
            'application_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'deadline_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'follow_up_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'recruiter_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Sarah Jenkins',
            }),
            'recruiter_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'recruiter@company.com',
            }),
            'recruiter_linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/recruiter-profile',
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Python, Django, REST API, React, Cloud',
            }),
            'resume_version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Software_Engineer_Resume_2026.pdf',
            }),
            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Key responsibilities, stack requirements, bonus qualifications...',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Interview prep notes, referrals, questions to ask...',
            }),
        }


class ApplicationTimelineForm(forms.ModelForm):
    class Meta:
        model = ApplicationTimeline
        fields = ['stage_title', 'event_date', 'notes']
        widgets = {
            'stage_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. HR Recruiter Screen, Technical Coding Round, System Design...',
                'required': True,
            }),
            'event_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Feedback, topics discussed, interviewers, takeaways...',
            }),
        }
