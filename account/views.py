from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout;
from django.contrib.auth.models import User
from django.contrib import messages,auth
from .form import signup
from Blog.form import updatedata,Userform
 
def signin(request):
	if not request.user.is_authenticated:
		if request.method=="POST":
			if request.POST['email'].strip() and  request.POST['password']:
				try:
					user=User.objects.get(email=request.POST['email'])
					auth.login(request,user)
					if request.POST["next"] !="":
						return redirect(request.POST.get('next'));
					else:
						return redirect("/user/account/mypost/");        
					return redirect("/user/account/mypost/");
				except User.DoesNotExist:
					messages.error(request,"User Does't Exist");
					return render(request,"signin.html");
			else:
				messages.error(request,"Empty field");
				return render(request,"signin.html")
		else:
			return render(request,'signin.html')
	else:
		return redirect("/user/account/mypost/");
	
def Signup(request):
	if not request.user.is_authenticated:
		if request.method=="POST":
			form=signup(request.POST or None) 
			if form.is_valid():
				form.save();
				return redirect('/user/account/mypost/')
			else:
				messages.error(request,form.errors)
				return render(request,'signup.html');
		else:
			form=signup();
			return render(request,"signup.html",{"form":form})
		return render(request,'signup.html')
	else:
		return redirect("/user/account/mypost/");


def myprofile(request):
	if request.method=="POST":
		form=updatedata(request.POST or None,request.FILES or None, instance=request.user.userprofile or None);
		form1=Userform(request.POST or None,instance=request.user or None);
		if form.is_valid() and form1.is_valid():
			form.save();
			form1.save();
			return redirect('/user/account/myprofile/');
		else:
			messages.error(request,form.errors)
			messages.error(request,form1.errors)
			return redirect('/user/account/myprofile/');
	else: 
		form=updatedata( instance=request.user.userprofile);
		form1=Userform(instance=request.user);
		return render(request,'Myprofile.html',{"form":form,"form1":form1});
	return render(request,'Myprofile.html')
	

def logout_view(request):
    logout(request)
    return redirect('/signin');