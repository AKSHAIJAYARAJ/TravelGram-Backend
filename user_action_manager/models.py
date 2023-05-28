from django.db import models

# Create your models here.

class UserModel(models.Model):

    user_id = models.AutoField(primary_key=True,unique=True)
    user_phone_number = models.CharField(max_length=13,null=True,blank=True)
    user_email = models.CharField(max_length=150,null=True,blank=True)
    user_pass_word = models.CharField(max_length=100,null=True,blank=True)
    user_created_on = models.DateTimeField(auto_now_add=True)
    user_modified_on = models.DateTimeField(auto_now_add=True)
    user_login_status = models.BooleanField(default=False)
    user_is_active = models.BooleanField(default=True)

 
    
