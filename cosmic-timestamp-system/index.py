"""
Vercel serverless function to serve the frontend
"""
import os

def handler(request):
    """Serve index.html for all non-API routes"""
    # Get the path to templates directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, 'templates', 'index.html')
    
    try:
        # Read and return the HTML file
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html; charset=utf-8',
                'Cache-Control': 'public, max-age=0, must-revalidate'
            },
            'body': html_content
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Error loading page: {str(e)}'
        }

