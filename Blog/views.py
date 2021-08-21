from django.shortcuts import render
from .form import Postartical 
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.db.models import Q
from taggit.models import Tag
from django.template.defaultfilters import slugify
from .models import PostArtical
from django.contrib.auth.models import User
from .models import Following;
from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.views.generic.base import RedirectView
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
import json
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.contrib import messages
from django.contrib import messages

@login_required
def following(request):
	user=Following.objects.get(user=request.user);
	followed_user=[i for i in user.followed.all()];
	followed_user.append(request.user);
	posts=PostArtical.objects.filter(user__in=followed_user).order_by("-id");
	return render(request,'following.html',{"posts":posts})

def Home(request):
	Trending_post=PostArtical.objects.order_by('hit')[:8]
	alltags=PostArtical.tags.most_common();
	Alldata=PostArtical.objects.all().order_by('-date');
	return render(request,'home.html',{"Alldata":Alldata,
										"Trending_post":Trending_post,
										'alltags':alltags
		});

def about(request):
	return render(request,'about.html');

@login_required
def mypost(request):
	user = request.user
	data = PostArtical.objects.filter(user=user).order_by("-id")
	return render(request,'allpost.html',{"data":data})

@login_required
def upload(request):
	user=request.user;
	alltags=PostArtical.tags.most_common();
	if request.method=="POST":
		user=request.user
		form=Postartical(request.POST or None,request.FILES or None);
		common_tags = PostArtical.tags.most_common()[:4]
		if form.is_valid():
			obj = form.save(commit=False) 
			obj.user = request.user; 
			obj.save()
			form.save_m2m()
			return redirect('/user/account/mypost/');
		else:
			messages.error(request,form.errors)
			return redirect('/user/account/upload/');
	else: 
		form=Postartical();
		return render(request,'writepost.html',{"form":form,'alltags':alltags});
	return render(request,'writepost.html',{'alltags':alltags})
 

def DiplayImages(request,username,slug):
	user=User.objects.filter(username=username);
	Data=None;
	if user and request.user.is_authenticated:
		user=user[0]
		Data=Following.objects.filter(user=request.user,followed=user);

	
	following_obj=Following.objects.get(user__username=username).follower.count();
	usernamedata=User.objects.get(username=username)
	queryset=PostArtical.objects.get(slug=slug);

	hit_count = HitCount.objects.get_for_object(queryset)
	hit_count_response = HitCountMixin.hit_count(request, hit_count)

	data = PostArtical.objects.filter(user__username=username).order_by('-date')[:6];
	return render(request,"Post.html",{"queryset":queryset,
														'data':data,
														'usernamedata':usernamedata,
														'Data':Data,
														"following_obj":following_obj,
														"hit_count_response":hit_count_response
														})
@login_required
def follow(request,username):
	main_user=request.user;
	to_follow=User.objects.get(username=username);
	# if already following user
	following=Following.objects.filter(user=main_user,followed=to_follow);
	is_following=True if following else False;

	if is_following:
		Following.unfollow(main_user,to_follow);
		is_following=False
	else:
		Following.follow(main_user,to_follow)
		is_following=True;

	resp={
	"following":is_following
	}
	response=json.dumps(resp);
	return HttpResponse(response)


class PostRedirectView(RedirectView):
	def get_redirect_url(self,*args,**kwargs):
		slug=self.kwargs.get('slug');
		print(slug)
		obj=get_object_or_404(PostArtical,slug=slug);
		usr_=obj.get_detail_url()
		user=self.request.user;
		if user.is_authenticated:
			if user in obj.like.all():
				obj.like.remove(user);
			else:
				obj.like.add(user)
		return usr_

 
class PostAPIRedirectView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request,slug=None, username=None, format=None):
    	
    	obj=get_object_or_404(PostArtical,slug=slug);
    	usr_=obj.get_api_like_url()
    	user=self.request.user;
    	updated=False;
    	liked=False
    	if user.is_authenticated:
    		if user in obj.like.all():
    			liked=False;
    			obj.like.remove(user);
    		else:
    			liked=True
    			obj.like.add(user);
    		updated=True
    		counts=obj.like.count()
    	data={"updated":updated,'liked':liked,"likescount": counts}
    	return Response(data)

class SaveAPIRedirectView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request,slug=None, username=None, format=None):
    	#slug=self.kwargs.get('slug');
    	obj=get_object_or_404(PostArtical,slug=slug);
    	usr_=obj.get_api_save_url()
    	user=self.request.user;
    	updated=False;
    	saved=False;
    	if user.is_authenticated:
    		if user in obj.save_post.all():
    			saved=False;
    			obj.save_post.remove(user);
    		else:
    			saved=True
    			obj.save_post.add(user);
    		updated=True
    		
    	datasave={"updated":updated,'saved':saved}
    	return Response(datasave)


@login_required
def saveImg(request):
	user=request.user;
	queryset = PostArtical.objects.filter(save_post=request.user).distinct().order_by('-id')
	return render(request,'save.html',{'queryset':queryset})

@login_required
def LikePost(request):
	user=request.user;
	queryset = PostArtical.objects.filter(like=request.user).distinct().order_by('-id')
	return render(request,'like.html',{'queryset':queryset}) 

def detail_view(request, slug):
    alltagsdata = get_object_or_404(Tag, slug=slug)
    posts = PostArtical.objects.filter(tags=alltagsdata).order_by('-id')
    return render(request, 'Tagpost.html', {'alltagsdata':posts})


def Search(request):
	q=request.GET['query']
	if len(q)>78:
		allpost=PostArtical.objects.none();
	else:
		allpostTitle=PostArtical.objects.filter(tags__name__icontains=q)
		print(allpostTitle)
		allpostcontent=PostArtical.objects.filter(Title__icontains=q);
		allpost=allpostTitle.union(allpostcontent)
	if allpost.count()==0:
		 messages.error(request, 'No search Result Found try again')
	if q=="":
		messages.error(request, 'Enter the value what you want!')
		allpost=PostArtical.objects.none();
	data={'allpost':allpost,'query':q}
	return render(request,'myaccountdata/Search.html',data)


def userdata(request,username):
	user=User.objects.filter(username=username);
	Data=None;
	if user and  request.user.is_authenticated:
		user=user[0]
		Data=Following.objects.filter(user=request.user,followed=user);
	Imagecount = PostArtical.objects.filter(user__username=username).count()
	queryset=PostArtical.objects.filter(user__username=username).aggregate(total_likes=Count('like'))['total_likes'] or 0
	print(queryset)
	data = PostArtical.objects.filter(user__username=username).order_by("-id")
	Userdata=User.objects.get(username=username)
	following_obj=Following.objects.get(user__username=username).follower.count();
	following=Following.objects.get(user__username=username).followed.count();
	
	return render(request,'user.html',{'Userdata':Userdata,
														'data':data,
														"Imagecount":Imagecount,
														"following_obj":following_obj,
														'Data':Data,
														"queryset":queryset,
														'following':following
														})


