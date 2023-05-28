from rest_framework.serializers import ModelSerializer
from .models import UserModel


class UserActionManagerSerializer(ModelSerializer):

    class Meta:
        model = UserModel
        fields = "__all__"