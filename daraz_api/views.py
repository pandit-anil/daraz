from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet

class CategoryView(APIView):
    
    def get(self, request):
        cate = Category.objects.all()
        serializer = CategorySerializer(cate, many= True)
        return  Response( serializer.data, status=status.HTTP_200_OK) 
    
    def post(self, request):
        serializer = CategorySerializer(data= request.data) 
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        category_name = serializer.validated_data.get('name')
        if Category.objects.filter(name = category_name ).exists():
            return Response({'status':"Already Exists"})
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request):
        cate = Category.objects.get(id = request.data.get('id'))
        serializer = CategorySerializer(cate, data=request.data, partial = True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
        
        name = serializer.validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            return Response({'status':"Already Exists"})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):

            id = request.GET.get('id')
            print(id)
            cate = Category.objects.get(id = id)
            
            cate.delete()
            return Response({'status':200, 'message':'Successfully Deleted'})

        
class CategoryViewCRUD(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer