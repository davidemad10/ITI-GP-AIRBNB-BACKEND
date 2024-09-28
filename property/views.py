# property/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import AllowAny

class GeocodeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({"error": "Missing query parameter 'q'."}, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = settings.OPENCAGE_API_KEY
        url = 'https://api.opencagedata.com/geocode/v1/json'
        params = {'q': query, 'key': api_key}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
