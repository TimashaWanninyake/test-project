# MongoDB and TalentHub Configuration Guide

## Step 1: MongoDB Connection Setup

### 1.1 Install MongoDB Compass (if not already installed)
- Download from: https://www.mongodb.com/products/compass
- Install and open MongoDB Compass

### 1.2 Connect to TalentHub MongoDB
1. Open MongoDB Compass
2. Click "New Connection"
3. Enter the MongoDB URL provided by TalentHub team in this format:
   ```
   mongodb://username:password@host:port/database
   ```
   OR
   ```
   mongodb+srv://username:password@cluster.mongodb.net/database
   ```
4. Click "Connect"

### 1.3 Update Django Settings
Once you have the MongoDB URL, update the settings in:
`intern_logbook_analysis/settings.py`

Replace these values:
```python
MONGODB_SETTINGS = {
    'CONNECTION_STRING': 'YOUR_MONGODB_URL_HERE',  # Replace with actual URL
    'DATABASE_NAME': 'YOUR_DATABASE_NAME_HERE',    # Replace with actual DB name
}

TALENTHUB_API_SETTINGS = {
    'BASE_URL': 'http://localhost:5000/api',  # Replace with actual Node.js URL
    'TIMEOUT': 30,
}
```

## Step 2: Install Required Packages

Run these commands in your terminal:
```powershell
# Install MongoDB packages
pip install pymongo dnspython

# Install HTTP requests package (if not already installed)
pip install requests

# Install CORS support
pip install django-cors-headers
```

## Step 3: Test the Connection

### 3.1 Start Django Server
```powershell
python manage.py runserver
```

### 3.2 Test Endpoints
Open browser or use Postman to test:

1. Health Check:
   ```
   GET http://127.0.0.1:8000/api/health/
   ```

2. MongoDB Info:
   ```
   GET http://127.0.0.1:8000/api/mongodb-info/
   ```

3. Get All Interns:
   ```
   GET http://127.0.0.1:8000/api/interns/
   ```

## Step 4: API Usage Examples

### 4.1 From Node.js Backend to Django

```javascript
// Node.js code to call Django analytics
const axios = require('axios');

const analyzeIntern = async (internId) => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/analyze/', {
            intern_id: internId,
            analysis_type: 'performance'
        });
        
        console.log('Analysis result:', response.data);
        return response.data;
    } catch (error) {
        console.error('Analysis failed:', error.response.data);
    }
};
```

### 4.2 From Django to Node.js Backend

```python
# In your Django views
from .talenthub_client import talenthub_client

# Send analysis results back to TalentHub
result = talenthub_client.send_analysis_results({
    'intern_id': intern_id,
    'analysis_type': 'sentiment',
    'results': analysis_data
})
```

## Step 5: Common TalentHub Database Structures

Typical MongoDB collections in TalentHub might be:
- `users` (contains intern profiles)
- `logbooks` or `logbook_entries` (contains daily logs)
- `evaluations` (contains performance evaluations)
- `tasks` or `assignments` (contains assigned tasks)

## Step 6: Troubleshooting

### Connection Issues:
1. Check if MongoDB URL is correct
2. Verify network access to MongoDB server
3. Check authentication credentials
4. Ensure Django server can reach Node.js backend

### API Issues:
1. Check CORS settings
2. Verify endpoint URLs
3. Check request/response formats
4. Monitor Django logs for errors

## Step 7: Next Steps

1. Get MongoDB URL from TalentHub team
2. Update settings.py with actual values
3. Test connections using health endpoints
4. Implement your specific analysis logic
5. Set up proper error handling and logging