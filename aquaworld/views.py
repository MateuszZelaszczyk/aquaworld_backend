from django.shortcuts import render
from .models import Aquariums, Posts, Users, Fish, Plants, Equipments, Fertilization, Ground, Comments, PostImage, Users, FriendRequest, user_push_token
from django.conf import settings
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import AquariumsSerial, PostsSerial, FishSerial, PlantSerial, EquipmentSerial, FertilizationSerial, GroundSerial, UpdateUserSerializer,UpdateUserAvatarSerial, CommentsSerial, UsersSerial, TokenSerial, MyTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from .firebase import send_push_notification
from rest_framework_simplejwt.views import TokenObtainPairView

User =get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class AqariumView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = AquariumsSerial
    queryset =Aquariums.objects.all()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        my_aquariums = Aquariums.objects.filter(user=self.request.user)
        return my_aquariums
    
@api_view(["GET", "POST"])
def Post_info(request):
    if request.method=='GET':
        posts = Posts.objects.filter(isPublic=True).values('id','title', 'describe','user_id__firstname','user_id__lastname','user_id__image', 'user_id__location', 'user_id__province').extra({'comments':Comments.objects.all().values('id', 'text')})
        for post in posts:
            post['comments']=Comments.objects.filter(post=post['id']).values('id','text','user__firstname', 'user__lastname', 'user__image')
            post['images'] =PostImage.objects.filter(post=post['id']).values('id','image')
        return Response({"posts":posts})

class PostView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class= PostsSerial
    def perform_create(self, serializer):
        comment=serializer.save(user=self.request.user)


class CommentsView(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerial
    def perform_create(self, serializer):
        title="Dodano komentarz"
        comm=serializer.save(user=self.request.user)
        to_user = comm.post.user
        if to_user!= self.request.user:
            message=f"{comm.user.firstname} {comm.user.lastname} skomentował/a Twój post"  
            print(to_user)
            send_push_notification(to_user,title, message)
class FishView(viewsets.ModelViewSet):
    queryset = Fish.objects.all()
    serializer_class = FishSerial
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data["fish"], many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
class PlantsView(viewsets.ModelViewSet):
    queryset = Plants.objects.all()
    serializer_class = PlantSerial
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data["plants"], many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

class EquipmentView(viewsets.ModelViewSet):
    queryset = Equipments.objects.filter()
    serializer_class =EquipmentSerial

class FertilizationView(viewsets.ModelViewSet):
    queryset = Fertilization.objects.all()
    serializer_class = FertilizationSerial
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data["fertilizer"], many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

class GroundView(viewsets.ModelViewSet):
    queryset =Ground.objects.all()
    serializer_class = GroundSerial
    print(HttpResponse)

class UpdateProfileView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer


@api_view(["GET"])
def GetUsers(request):
    user = request.user
    friends = request.user.friends.all()
    queryset = Users.objects.exclude(id=request.user.pk)
    queryset = queryset.exclude(id__in=[friend.pk for friend in friends])
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    queryset = queryset.exclude(id__in=[friend_request.from_user.pk for friend_request in friend_requests]).values('id','firstname','lastname','location','province','image')
    return Response(queryset)

class UpdateUserAvatarView(viewsets.ModelViewSet):
    queryset =User.objects.all();
    
    serializer_class = UpdateUserAvatarSerial
    def get_queryset(self):
        user = User.objects.filter(email=self.request.user)
        return user
@api_view(["GET"])
def UserInfo(request):
    if(request.method=="GET"):
        user = Users.objects.filter(email=request.user).values('firstname', 'lastname',  'image', 'phone','location', 'province')
        id=request.user.pk
        return Response({"user":user, "id":id})


@api_view(["GET"])
def AquariumData(request,id):
    if request.method == 'GET':
        fish = Fish.objects.filter(aquarium=id).values("name", "quantity","id")
        plants = Plants.objects.filter(aquarium=id).values("name", "quantity","id")
        fertilizers = Fertilization.objects.filter(aquarium=id).values("name", "dose","id")
        equipments = Equipments.objects.filter(aquarium=id).values("lighting","filtering","heating", "CO2","control", "other")
        ground = Ground.objects.filter(aquarium=id).values('base', 'substrate')
        aquarium =Aquariums.objects.filter(id=id).values("name", "type", "capacity", "height", "depth", "length", "startDate", "image")

        
        return Response({"aquarium":aquarium, "fish":fish, "plants":plants, "fertilizers":fertilizers, "equipments":equipments,"base":ground})
    return HttpResponse('info')

@api_view(["GET"])
def GroundInfo(request,id):
    if request.method == 'GET':
        ground = Ground.objects.filter(aquarium=id).values('base', 'substrate', 'id')
        isGround = ground.exists();
        return Response({"isGround":isGround, 'ground':ground})
    return HttpResponse('Groundinfo')

@api_view(["GET"])
def EquipmentsInfo(request,id):
    if request.method == 'GET':
        equipments = Equipments.objects.filter(aquarium=id).values("lighting","filtering","heating", "CO2","control", "other",'id')
        isEquipments = equipments.exists();
        return Response({ "isEquipments":isEquipments, "equipments":equipments})
    return HttpResponse('Equipmentinfo')


@api_view(["POST"])
def Send_request(request, id):
    from_user = request.user
    to_user = Users.objects.get(id=id)
    title = "Zaproszenie do znajomych"
    message = f"{from_user.firstname} {from_user.lastname} wysłał/a Ci zaproszenie do znajomych"
    if from_user == to_user:
        return Response({"error": "Wysłałeś zaproszenie do siebie."})
    if to_user in from_user.friends.all():
        return Response({"error": "Użytkownik jest już Twoim znajomym."})
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return Response({"error": "Zaprosznie zostało już wysłane"})
    FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    send_push_notification(to_user,title, message)
    return Response({"success": "Zaproszenie do znajomych zostało wysłane."})


@api_view(["POST"])
def Accept_friend(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    friend_request.from_user.friends.add(friend_request.to_user)
    friend_request.delete()
    return Response({"success": "Zaproszenie zaakceptowane."})


@api_view(["POST"])
def Reject_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    friend_request.delete()
    return Response({"success": "Zaproszenie odrzucone."})

@api_view(["POST"])
def Remove_friend(request, friend_id):
    friend = Users.objects.get(id=friend_id)
    if friend not in request.user.friends.all():
        return Response({"error": "Ten użytkownik nie jest Twoim znajomym"})
    friend.friends.remove(request.user)
    request.user.friends.remove(friend)
    return Response({"success": "Znajomy usunięty."})

@api_view(["GET"])
def Get_friends(request):
    user = request.user
    serializer = UsersSerial(user.friends.all(), many=True)
    return Response(serializer.data)


@api_view(["GET"])
def Get_friend_requests(request):
    user = request.user
    requests = user.received_requests.all()
    data = []
    for request in requests:
        serializer = UsersSerial(request.from_user, many=False)
        data.append({
            "user": serializer.data,
            "request_id": request.id
        })
    return Response(data)

@api_view(["POST"])
def CheckToken(request):
        token=request.data.get('token')
        print(token);
        if user_push_token.objects.filter(token=token).exists():
            return Response({"message": "Ten token już istnieje"})
        if token=="":
            return Response({"error":"Token is empty"})
        user_push_token.objects.create(user=request.user, token=request.data.get('token'))
        return Response({"message":"Dodano token"})


        
    
    



