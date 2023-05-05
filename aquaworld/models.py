from django.db import models
from django.conf import settings
from django.db.models.expressions import Case
from django.db.models.deletion import CASCADE
from django.db.models.fields import Field
import django.utils.timezone as timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager, User

class UserAccountManager(BaseUserManager):
    def create_user(self, firstname, lastname, email, image=None, phone=None, password=None, location=None, province=None):
        email=self.normalize_email(email)
        user=self.model(email=email, firstname=firstname, lastname=lastname, phone=phone, image=image, location=location, province=province)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, firstname, lastname, email, image=None, phone=None, password=None, location=None, province=None):
        user=self.model(email=email, firstname=firstname, lastname=lastname, phone=phone, image=image, location=location, province=province)
        is_active=True
        user.set_password(password)
        user.save()
        is_staff = True
        return user

class Users(AbstractBaseUser, PermissionsMixin):
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email = models.EmailField(max_length=40, unique=True)
    phone =models.CharField(max_length=20, unique=True, blank=True, null=True)
    location=models.CharField(max_length=100, default="", blank=True, null=True)
    province= models.CharField(max_length=30, default="", blank=True, null=True)
    image = models.ImageField(upload_to='profile/', default='profile/Avatar.png')
    is_active=models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects=UserAccountManager()
    friends = models.ManyToManyField("self", related_name='requested_friend',  blank=True, symmetrical=False)
    friend_requests = models.ManyToManyField("self", related_name='requested_friend_of', blank=True, symmetrical=False, through="FriendRequest")

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['firstname','lastname','password']

    def __str__(self):
        return self.email
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="sent_requests")
    to_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="received_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("from_user", "to_user")
        
class  Aquariums(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    name =models.CharField(max_length=40)
    type = models.CharField(max_length=20)
    capacity = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    startDate = models.DateField()
    image = models.ImageField(upload_to='images/',default='profile/Avatar.png')
    def __str__(self):
        return self.name
    
class Fish(models.Model):
    aquarium = models.ForeignKey(Aquariums, on_delete=models.CASCADE, related_name="AquaFish")
    name = models.CharField(max_length=30)
    quantity =models.IntegerField(default=0)

    class Meta:
        unique_together=("aquarium", "name")
    def __str__(self):
        return self.name
    
class Plants(models.Model):
    aquarium = models.ForeignKey(Aquariums, on_delete=models.CASCADE, related_name="AquaPlants")
    name = models.CharField(max_length=50)
    quantity =models.IntegerField(default=0)
    class Meta:
        unique_together=("aquarium", "name")
    def __str__(self):
        return self.name
    
class Equipments(models.Model):
    aquarium =models.OneToOneField(Aquariums, on_delete=models.CASCADE, related_name="AquaEquipment")
    lighting = models.CharField(max_length=100, default="")
    filtering = models.CharField(max_length=80, default="")
    heating = models.CharField(max_length=60, default="")
    CO2 = models.CharField(max_length=150, default="", blank=True)
    control = models.CharField(max_length=100, default="", blank=True)
    other = models.CharField(max_length=150, default="", blank=True)
    def __str__(self):
        return self.aquarium

class Ground(models.Model):
    aquarium = models.OneToOneField(Aquariums, on_delete=models.CASCADE, related_name="AquaGround")
    substrate = models.CharField(max_length=80, default="", blank=True)
    base = models.CharField(max_length=80, default="", blank=True)
    def __str__(self):
        return self.base

class Fertilization(models.Model):
    aquarium = models.ForeignKey(Aquariums, on_delete=models.CASCADE, related_name="AquaFert")
    name = models.CharField(max_length=80, default="")
    dose = models.FloatField(default=0)

    class Meta:
        unique_together=("aquarium", "name")
    def __str__(self):
        return self.name

    
class Posts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    title= models.CharField(max_length=60)
    describe = models.CharField(max_length=2000)
    isPublic = models.BooleanField(default=True)
    def __str__(self):
        return self.title

class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments", default=None)
    text = models.TextField(blank=False, max_length=1000)

class PostImage(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/",blank=True, null=True)
    def __str__(self):
        return self.post.title
    
class  user_push_token(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    token =models.CharField (max_length=200, unique=True)
    def __str__(self):
        return self.token