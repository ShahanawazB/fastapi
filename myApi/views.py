from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class HelloApiView(APIView):
    def get(self, request, format=None):
        response_obj = ['hello', 'how you', 'what']
        return Response({'message' : 'Success', 'obj' : response_obj})
