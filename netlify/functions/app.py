import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from flask import Request, Response

def handler(event, context):
    """Netlify function handler for Flask app"""
    # Convert Netlify event to Flask request
    with app.test_client() as client:
        # Build the request
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        # Make the request
        if body:
            response = client.open(
                path,
                method=method,
                headers=headers,
                data=body
            )
        else:
            response = client.open(
                path,
                method=method,
                headers=headers
            )
        
        # Convert Flask response to Netlify response
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }
