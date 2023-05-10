from django.http import JsonResponse
from .models import Customer,Product
from .serializers import CustomerSerializer,ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date,timedelta
@api_view(['GET','POST'])
def customer_list(request,format=None):
#get all clients and serialize them and return Json file

    if request.method=='GET':
        customer=Customer.objects.all()
        serializer=CustomerSerializer(customer,many=True)
        return Response(serializer.data)
    
    if request.method=='POST':
        serializer=CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
@api_view(['GET','POST'])
def product_list(request,format=None):
#get all product and serialize them and return Json file

    if request.method=='GET':
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)
    
    if request.method=='POST':
        serializer=ProductSerializer(data=request.data)
        

        if serializer.is_valid():
            
            expired = date.today() - timedelta(days=60)
            if serializer.validated_data['registered_date'] <= expired:
                serializer.validated_data['active'] = False
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
##CUSTOMER     
@api_view(['GET','PUT','DELETE'])
def customer_detail(request,id,format=None):
    try:
       customer= Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)
    
    elif request.method=='PUT':
        serializer=CustomerSerializer(customer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method=='DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET','PUT','DELETE'])
def product_detail(request,id,format=None):
    try:
       product= Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method=='PUT':
        serializer=ProductSerializer(product,data=request.data)
        expired=date.today()-timedelta(days=60)

        if product.registered_date<=expired and serializer.is_valid():
            
            serializer.validated_data['active']=False
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method=='DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)