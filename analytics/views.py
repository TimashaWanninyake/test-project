"""
Views for analytics API endpoints
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from datetime import datetime

from .mongo_service import mongo_service
from .talenthub_client import talenthub_client

logger = logging.getLogger(__name__)

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    mongo_status = mongo_service.test_connection()
    talenthub_status = talenthub_client.test_connection()
    
    return Response({
        "status": "healthy",
        "service": "Django Analytics Backend",
        "connections": {
            "mongodb": "connected" if mongo_status else "disconnected",
            "talenthub_api": "connected" if talenthub_status else "disconnected"
        },
        "timestamp": datetime.now().isoformat()
    })

@api_view(['GET'])
def get_mongodb_info(request):
    """Get MongoDB connection info and collections"""
    try:
        collections = mongo_service.get_collections()
        return Response({
            "success": True,
            "data": {
                "connected": mongo_service.test_connection(),
                "collections": collections,
                "database": mongo_service.db.name if mongo_service.db else None
            }
        })
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_interns(request):
    """Get all interns from MongoDB"""
    try:
        interns = mongo_service.get_all_interns()
        return Response({
            "success": True,
            "data": {
                "interns": interns,
                "total_count": len(interns)
            },
            "source": "mongodb",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error fetching interns from MongoDB: {str(e)}")
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_intern_details(request, intern_id):
    """Get specific intern details"""
    try:
        intern = mongo_service.get_intern_by_id(intern_id)
        if not intern:
            return Response({
                "success": False,
                "error": "Intern not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "success": True,
            "data": {
                "intern": intern
            }
        })
    except Exception as e:
        logger.error(f"Error fetching intern {intern_id}: {str(e)}")
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_intern_logbooks(request, intern_id):
    """Get logbook entries for a specific intern"""
    try:
        limit = request.GET.get('limit', 100)
        logbook_entries = mongo_service.get_logbook_entries(intern_id, int(limit))
        
        return Response({
            "success": True,
            "data": {
                "intern_id": intern_id,
                "logbook_entries": logbook_entries,
                "total_count": len(logbook_entries)
            }
        })
    except Exception as e:
        logger.error(f"Error fetching logbooks for intern {intern_id}: {str(e)}")
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def analyze_intern_basic(request):
    """
    Basic analysis endpoint - placeholder for your analysis logic
    Expected payload: {"intern_id": "string", "analysis_type": "string"}
    """
    try:
        data = request.data
        intern_id = data.get('intern_id')
        analysis_type = data.get('analysis_type', 'basic')
        
        if not intern_id:
            return Response({
                "success": False,
                "error": "intern_id is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get intern data
        intern = mongo_service.get_intern_by_id(intern_id)
        if not intern:
            return Response({
                "success": False,
                "error": "Intern not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get logbook entries
        logbook_entries = mongo_service.get_logbook_entries(intern_id)
        
        # Basic analysis (you can expand this)
        analysis_result = {
            "intern_id": intern_id,
            "analysis_type": analysis_type,
            "intern_name": intern.get('name', 'Unknown'),
            "total_logbook_entries": len(logbook_entries),
            "analysis_date": datetime.now().isoformat(),
            "summary": {
                "entries_count": len(logbook_entries),
                "has_data": len(logbook_entries) > 0
            }
        }
        
        # If you want to send results back to TalentHub Node.js backend
        # talenthub_client.send_analysis_results(analysis_result)
        
        return Response({
            "success": True,
            "data": analysis_result
        })
        
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def send_to_talenthub(request):
    """Send data to TalentHub Node.js backend"""
    try:
        data = request.data
        endpoint = data.get('endpoint', '')
        payload = data.get('payload', {})
        
        if not endpoint:
            return Response({
                "success": False,
                "error": "endpoint is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Make API call to TalentHub
        result = talenthub_client._make_request('POST', endpoint, data=payload)
        
        return Response({
            "success": True,
            "data": {
                "talenthub_response": result,
                "sent_data": payload
            }
        })
        
    except Exception as e:
        logger.error(f"Error sending to TalentHub: {str(e)}")
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Legacy function - keeping for compatibility
def analyze_intern(request):
    """Legacy analyze function"""
    return JsonResponse({
        "message": "Please use the new API endpoints",
        "available_endpoints": [
            "/api/analytics/health/",
            "/api/analytics/interns/",
            "/api/analytics/intern/{id}/",
            "/api/analytics/logbooks/{intern_id}/",
            "/api/analytics/analyze/"
        ]
    })