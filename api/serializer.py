from .models import Profile, Content
from rest_framework import serializers
from django.contrib.auth.models import User
from djangoflutterwave.models import FlwPlanModel, FlwTransactionModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True,'required':True}}

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlwPlanModel
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlwTransactionModel
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault(), source="user.username",)
    access_plan =PlanSerializer( read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user','profile_pic','gender', 'mobile', 'access_plan')




class ContentSerializer(serializers.ModelSerializer):
    content_accessplan =PlanSerializer( read_only=True)

    class Meta:
        model = Content
        fields = ('id', 'title','description','content_file', 'content_accessplan','created_at', 'updated_on')

