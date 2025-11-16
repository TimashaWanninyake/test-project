"""
Service for making API calls to TalentHub Node.js backend
"""
import requests
import json
from typing import Dict, List, Optional, Any
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TalentHubAPIClient:
    """Client for communicating with TalentHub Node.js backend"""
    
    def __init__(self):
        self.base_url = settings.TALENTHUB_API_SETTINGS['BASE_URL']
        self.timeout = settings.TALENTHUB_API_SETTINGS['TIMEOUT']
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Make HTTP request to TalentHub backend"""
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for {endpoint}")
            return {"error": "Request timeout"}
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error for {endpoint}")
            return {"error": "Connection failed"}
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for {endpoint}: {e}")
            return {"error": f"HTTP error: {e.response.status_code}"}
        
        except Exception as e:
            logger.error(f"Unexpected error for {endpoint}: {str(e)}")
            return {"error": str(e)}
    
    def get_intern_data(self, intern_id: str) -> Dict:
        """Get intern data from TalentHub"""
        return self._make_request('GET', f'/interns/{intern_id}')
    
    def get_all_interns(self) -> Dict:
        """Get all interns from TalentHub"""
        return self._make_request('GET', '/interns')
    
    def get_logbook_entries(self, intern_id: str, params: Optional[Dict] = None) -> Dict:
        """Get logbook entries for an intern"""
        return self._make_request('GET', f'/logbooks/intern/{intern_id}', params=params)
    
    def send_analysis_results(self, analysis_data: Dict) -> Dict:
        """Send analysis results back to TalentHub"""
        return self._make_request('POST', '/analytics/results', data=analysis_data)
    
    def notify_analysis_complete(self, intern_id: str, analysis_type: str, results: Dict) -> Dict:
        """Notify TalentHub that analysis is complete"""
        notification_data = {
            "intern_id": intern_id,
            "analysis_type": analysis_type,
            "results": results,
            "status": "completed"
        }
        return self._make_request('POST', '/analytics/notifications', data=notification_data)
    
    def test_connection(self) -> bool:
        """Test connection to TalentHub backend"""
        try:
            result = self._make_request('GET', '/health')
            return 'error' not in result
        except Exception:
            return False

# Global client instance
talenthub_client = TalentHubAPIClient()