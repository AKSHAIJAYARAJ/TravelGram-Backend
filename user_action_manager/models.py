from django.db import models

# Create your models here.

class UserModel(models.Model):

    user_id = models.AutoField(primary_key=True,unique=True)
    user_phone_number = models.CharField(max_length=13,null=True,blank=True)
    user_uid = models.CharField(max_length=100,null=True,blank=True)
    user_email = models.CharField(max_length=150,null=True,blank=True)
    user_password = models.CharField(max_length=500,null=True,blank=True)
    user_created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    user_modified_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    user_login_status = models.BooleanField(default=False,null=True,blank=True)
    user_is_active = models.BooleanField(default=True,null=True,blank=True)

# class UserGraphModel(models.Model):

#     first_name = models.CharField(max_length=200,null=True,blank=True,db_column='User.first_name')
#     last_name = models.CharField(max_length=200,null=True,blank=True,db_column='User.last_name')
#     gender = models.CharField(max_length=10,null=True,blank=True,db_column='User.gender')
#     nick_name = models.CharField(max_length=200,null=True,blank=True,db_column='User.nick_name')
#     user_id = models.IntegerField(db_column='User.id')

# class LocationGraphModel(models.Model):

#     location_name = models.CharField(max_length=200,null=True,blank=True,db_column='Location.name')
#     longitude = models.FloatField(null=True,blank=True,db_column='Location.longitude')
#     latitude = models.FloatField(null=True,blank=True,db_column='Location.latitude')
#     discription = models.CharField(max_length=20000,null=True,blank=True,db_column='Location.discription')
#     user = models.ForeignKey('UserGraphModel', on_delete=models.CASCADE, null=True, blank=True,db_column='Location.user')

# class LocationGraphConnectionModel(models.Model):
#     # Relation to get user who added a perticular location
#     from_location = models.ForeignKey(LocationGraphModel, related_name='edge', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(LocationGraphModel, related_name='reverse_edge', on_delete=models.CASCADE)
 
    
