from rest_framework import serializers



class LocationSerializer(serializers.Serializer):

    name = serializers.CharField(max_length = 250,allow_blank =True,allow_null = True,required = False)
    description = serializers.CharField(max_length = 10000,allow_blank =True,allow_null = True,required = False)
    latitude = serializers.FloatField(required = False)
    longitude = serializers.FloatField(required = False)
    hash_tags = serializers.CharField(max_length = 250,allow_blank =True,allow_null = True,required = False)
    user = serializers.CharField(max_length = 20,allow_blank =True,allow_null = True,required = False)
    created_on = serializers.DateTimeField(required = False)
    rated_person_id  = serializers.CharField(max_length = 20,allow_blank =True,allow_null = True,required = False)
    overall_rating = serializers.FloatField(required = False)
    location = serializers.CharField(max_length = 20,allow_blank =True,allow_null = True,required = False)
    likes = serializers.IntegerField(required = False)
    shares = serializers.IntegerField(required = False)