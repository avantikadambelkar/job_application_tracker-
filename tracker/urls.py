from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('kanban/', views.kanban_view, name='kanban'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('add/', views.application_create_view, name='application_create'),
    path('application/<int:pk>/', views.application_detail_view, name='application_detail'),
    path('application/<int:pk>/edit/', views.application_update_view, name='application_update'),
    path('application/<int:pk>/delete/', views.application_delete_view, name='application_delete'),
    path('application/<int:pk>/status/', views.quick_status_update_view, name='quick_status_update'),
    path('application/<int:pk>/timeline/add/', views.add_timeline_event_view, name='add_timeline_event'),
    path('export/csv/', views.export_csv_view, name='export_csv'),
    path('seed-demo/', views.seed_demo_data_view, name='seed_demo'),
]
