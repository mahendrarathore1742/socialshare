from django.urls import path
from .views import (PostRedirectView,PostAPIRedirectView,SaveAPIRedirectView)
from .views import Home,about,mypost,upload,DiplayImages,following,saveImg,follow,detail_view,Search,userdata,LikePost;

urlpatterns = [

     path("",Home,name="home"), 
     path("about/",about,name='about'),
     path("user/account/mypost/",mypost,name='mypost'),
     path('user/account/upload/',upload,name="upload"),
     path('post/<slug:username>/<slug:slug>/',DiplayImages,name='DiplayImages'),
     path('user/account/following/',following,name="following"),
     path('user/account/save/',saveImg,name='saveImg'),
     path('user/follow/<slug:username>',follow,name="follow"),
     path('post/<slug:username>/<slug:slug>/like',PostRedirectView.as_view(),name='like'),
	path('post/<slug:username>/<slug:slug>/like/api',PostAPIRedirectView.as_view(),name='like_api'),
	path('post/<slug:username>/<slug:slug>/save/api',SaveAPIRedirectView.as_view(),name='save_api'),
	path('Tags/<slug:slug>',detail_view,name="detail_view"),
	path('Search/data/',Search,name='Search'),
     path('user/<slug:username>/',userdata,name='userdata'),
     path('user/account/like/',LikePost,name='LikePost'),

	
]
  
