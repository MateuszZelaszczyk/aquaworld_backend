from django.db.models import fields
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from .models import Aquariums, Posts, PostImage, Users, Fish, Plants, Equipments, Ground, Fertilization, Comments

User =get_user_model()

class UserCreateSerial(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model=User
        fields="__all__"
class UsersSerial(serializers.ModelSerializer):
    class Meta(UserCreateSerializer.Meta):
        model: Users
        fields=('id','firstname', 'lastname','location', 'province', 'image')
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'phone','location', 'province')

    def update(self, instance, validated_data):
        instance.firstname = validated_data['firstname']
        instance.lastname = validated_data['lastname']
        instance.phone = validated_data['phone']
        instance.location = validated_data['location']
        instance.province = validated_data['province']
        instance.save()
        return instance
    
class UpdateUserAvatarSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('image',)
    def update(self, instance, validated_data):
        instance.image = validated_data['image']
        instance.save()
        return instance

class AquariumsSerial(serializers.ModelSerializer):
    class Meta:
        model= Aquariums
        fields="__all__"

class PostImgSerial(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = "__all__"

class PostsSerial(serializers.ModelSerializer):
    images = PostImgSerial(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child= serializers.ImageField(allow_empty_file=True, use_url=False),
        write_only=True,
        required=False,
    )
    class Meta:
        model = Posts
        fields=['id', 'title', 'isPublic', 'user', 'images', 'uploaded_images','describe']

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        post = Posts.objects.create(**validated_data)

        if uploaded_images:
            for image in uploaded_images:
                PostImage.objects.create(post=post, image=image)
        return post

class FishSerial(serializers.ModelSerializer):
    class Meta:
        model = Fish
        fields="__all__"

class PlantSerial(serializers.ModelSerializer):
    class Meta:
        model = Plants
        fields="__all__"

class EquipmentSerial(serializers.ModelSerializer):
    class Meta:
        model =Equipments
        fields="__all__"
    
class GroundSerial(serializers.ModelSerializer):
    class Meta:
        model = Ground
        fields="__all__"

class FertilizationSerial(serializers.ModelSerializer):
    class Meta:
        model = Fertilization
        fields="__all__"

class CommentsSerial(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields="__all__"