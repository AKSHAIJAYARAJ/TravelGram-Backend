# MODULE DETAILS
# __________________________________________________________________________________________________________________________
# MODULE NAME   : User Action Manager Views
# VERSION       : 1.0
# SYNOPSYS      : This module is handles views for user_action_manager.
# AUTHOR        : AKSHAI JAYARAJ
# CREATED ON    : 2023-MAY-28
# METHODS       : 
# 
# ENHANCEMENT HISTORY
# __________________________________________________________________________________________________________________________
# AUTHOR        : <AUTHOR>
# CREATED ON    : <CREATED ON>
# METHODS       : <METHODS>
# __________________________________________________________________________________________________________________________

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import permissions
from .user_manager import User


# Create your views here.

class SignInUpViewSet(APIView):

    def get(self,request):
        pass
    def post(self,request):
        try:
            response = User().log_in(data = request.data)
            return Response(data={"status":response["status"],"result":response["result"],'message':response["message"]},status=status.HTTP_200_OK)
        except:
            return Response(data={"status":"error","result":response,'message':'error'},status=status.HTTP_400_BAD_REQUEST)
    def put(self,request):
        pass
    def delete(self,request):
        pass

class UserRegistrationViewSet(APIView):
    
    def post(self,request):
        try:
            response = User().register(data = request.data)
            return Response(data={"status":response["status"],"result":response["result"],'message':response["message"]},status=status.HTTP_200_OK)
        except Exception as e:
            print("-----EPTN----",e)
            return Response(data={"status":"error","result":'','message':'error'},status=status.HTTP_400_BAD_REQUEST)

