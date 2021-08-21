from django.contrib.auth.models import User
from .models import  Userdata;
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import PostArtical
from django import forms;


class  updatedata(UserChangeForm):
	class Meta:
		model=Userdata;
		fields=("Profileimage",'FirstName','LastName','position','Aboutme')
 

class Userform(UserChangeForm):
	class Meta:
		model=User;
		fields=("username",'email')
		
class Postartical(forms.ModelForm):
	class Meta:
		model=PostArtical;
		fields=("Images","Title",'tags','Artical')