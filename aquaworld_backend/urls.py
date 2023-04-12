from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from aquaworld.views import AqariumView, PostView, Post_info, FishView, PlantsView, FertilizationView, GroundView, EquipmentView, AquariumData, UpdateProfileView, UserInfo, UpdateUserAvatarView, GroundInfo, EquipmentsInfo,CommentsView,GetUsers, Send_request, Accept_friend, Reject_request, Get_friends, Get_friend_requests, Remove_friend, CheckToken
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

route = routers.DefaultRouter()
route.register('aquariums', AqariumView, basename="aquariums")
route.register('posts', PostView, basename="posts")
route.register('fish', FishView, basename="fish")
route.register('plants', PlantsView, basename="plants")
route.register('fertilization', FertilizationView, basename='fertilization')
route.register('ground', GroundView, basename="ground")
route.register('equipments', EquipmentView, basename="equipments")
route.register('updateuser', UpdateProfileView, basename="users")
route.register('updateAvatar', UpdateUserAvatarView, basename="users")
route.register('comments', CommentsView, basename="comments")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include(route.urls)),
    path('api/postsinfo', Post_info),
    path('api/aquaInfo/<int:id>/', AquariumData),
    path('api/groundInfo/<int:id>/', GroundInfo),
    path('api/equipmentInfo/<int:id>/', EquipmentsInfo),
    path('api/userInfo/', UserInfo),
    path('api/sendrequest/<int:id>/', Send_request),
    path('api/acceptfriend/<int:request_id>/', Accept_friend),
    path('api/rejectrequest/<int:request_id>/', Reject_request),
    path('api/getfriends/', Get_friends),
    path('api/getfriendsrequest/', Get_friend_requests),
    path('api/removefriend/<int:friend_id>/', Remove_friend),
    path('api/sendnotification', Send_request),
    path('api/notifytokens/', CheckToken),
    path("api/users/", GetUsers),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),name ='token_refresh')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^.*',
                        TemplateView.as_view(template_name='index.html'))]
