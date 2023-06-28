from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LocationSerializer
from .location import Location
from rest_framework import status

class LocationViewSet(APIView):
    def __init__(self):
        self.user_serializer = LocationSerializer

    def post(self,request):
        print('================')
        try:
            validator = self.user_serializer(data=request.data)
            if validator.is_valid():
                uid = Location().post(location_data=validator.validated_data)
                return Response(data={'Status':"Ok",'Result':uid,'Message': "Location added"},status=status.HTTP_200_OK)
            else:
                return Response(data={'Status':"Error",'Result':'','Message': "Invalid data"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(data={'Status':"Error",'Result':'','Message': "Error"},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        try:
            location_id = request.query_params.get('location_id')
            location_data = Location().get(location_id=location_id)
            return Response(data={'Status':"Ok",'Result':location_data,'Message': "Location fetched"},status=status.HTTP_200_OK)
        except:
            return Response(data={'Status':"Error",'Result':'','Message': "Error"},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        try:
            location_id = request.query_params.get('location_id')
            validator = self.user_serializer(data=request.data)
            if validator.is_valid:
                uid = Location().put(location_data=validator.validated_data,location_id=location_id)
                return Response(data={'Status':"Ok",'Result':uid,'Message': "Location updated"},status=status.HTTP_200_OK)
            else:
                return Response(data={'Status':"Error",'Result':'','Message': "Invalid data"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={'Status':"Error",'Result':'','Message': "Error"},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        try:
            location_data = Location().get(location_id=request.query_params.get('location_id'))
            return Response(data={'Status':"Ok",'Result':location_data,'Message': "Location deleted"},status=status.HTTP_200_OK)
        except:
            return Response(data={'Status':"Error",'Result':'','Message': "Error"},status=status.HTTP_400_BAD_REQUEST)
