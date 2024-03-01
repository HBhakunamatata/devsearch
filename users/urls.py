

from django.urls import path
from . import views


urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.user_profile, name='user-profile'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('account/', views.userAccount, name='account'),
    path('account_edit/', views.editAccount, name='account-edit'),
    
    path('skill_create/', views.createSkill, name='skill-create'),
    path('skill_update/<str:pk>', views.updateSkill, name='skill-update'),
    path('skill_delete/<str:pk>', views.deleteSkill, name='skill-delete'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>', views.viewMessage, name='message'),
    path('create_message/<str:pk>', views.createMessage, name='create-message'),


]