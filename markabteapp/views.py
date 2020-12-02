from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


class OrderListView(ListAPIView):
    #get all order objects
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    #only authenticated users can access this view
    permission_classes = [IsAuthenticated]
    #For filtering the objects based on the (customer) field, and ordering the results
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['customer',]

class OrderCreateView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]
  
  #override the create view to force the current user to be added to the order as the (entered_by) field
    def perform_create(self, serializer):
        serializer.save(entered_by=self.request.user)

class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        my_data = request.data
        serializer = UserLoginSerializer(data=my_data)
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)