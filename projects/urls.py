from django.urls import path
from . import views


urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>', views.project, name='project'),
    
    path('project_create', views.project_create, name='project_create'),
    path('project_update/<str:pk>', views.project_update, name='project_update'),
    path('project_delete/<str:pk>', views.project_delete, name='project_delete'),

    # path('project_search', views.project_search, name='project_search'),

]