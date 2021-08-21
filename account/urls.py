from django.urls import path
from .views import signin,Signup,myprofile,logout_view
from django.contrib.auth import views as reset;
urlpatterns = [
     path('signin/',signin,name='signin'),
     path('signup/',Signup,name='signup'),
     path('accounts/password/reset/',reset.PasswordResetView.as_view(template_name='PasswordReset/paswordreset.html'),name='password_reset'),
     path('accounts/password/reset/done',reset.PasswordResetDoneView.as_view(template_name='PasswordReset/Done.html'),name='password_reset_done'),
     path('accounts/password/reset/confirm/<uidb64>/<token>',reset.PasswordResetConfirmView.as_view(template_name='PasswordReset/confirm.html'),name='password_reset_confirm'),
     path('accounts/password/reset/complete',reset.PasswordResetCompleteView.as_view(template_name='PasswordReset/passwordresetcomplete.html'),name='password_reset_complete'),
     path('user/account/myprofile/',myprofile,name='myprofile'),
     path('user/account/logout/',logout_view,name='logout_view'),
    
]
   
