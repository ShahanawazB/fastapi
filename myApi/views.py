from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myApi import serializers
from profiles.settings import DATABASES

# Create your views here.

class HelloApiView(APIView):
    serializer_class = serializers.HelloSerializer
    def get(self, request, format=None):
        response_obj = ['hello', 'how you', 'what']
        return Response({'message' : 'Success', 'obj' : response_obj})
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'hello {name }'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        return Response({"this is put method"})
    
    def patch(self, request, pk=None):
        return Response({"this is patch method"})
    
    def delete(self, request, pk=None):
        return Response({"this is delete method"})
