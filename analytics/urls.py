"""
URL configuration for analytics app
"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Health and connection checks
    path('health/', views.health_check, name='health_check'),
    path('mongodb-info/', views.get_mongodb_info, name='mongodb_info'),
    
    # Intern data endpoints
    path('interns/', views.get_all_interns, name='get_all_interns'),
    path('intern/<str:intern_id>/', views.get_intern_details, name='get_intern_details'),
    path('logbooks/<str:intern_id>/', views.get_intern_logbooks, name='get_intern_logbooks'),
    
    # Analysis endpoints
    path('analyze/', views.analyze_intern_basic, name='analyze_intern_basic'),
    
    # TalentHub communication
    path('send-to-talenthub/', views.send_to_talenthub, name='send_to_talenthub'),
    
    # Legacy endpoint
    path('analyze-legacy/', views.analyze_intern, name='analyze_intern_legacy'),
]
