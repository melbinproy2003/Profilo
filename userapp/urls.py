from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexpage, name='index'),
    path('login/', views.userlogin, name='signin'),
    path('registration/', views.userregistration, name='signup'),
    path('homepage/', views.userhome, name='userhome'),
    path('logout/', views.logout_view, name='logout'),
    path('adminhome/', views.webadmin, name='webadmin'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile/<int:profile_id>/', views.profile_detail, name='profile_detail'),
    path('projects/', views.listprojects, name='projects'),
    path('addproject/', views.projects, name='addproject'),
    path('projects/update/<int:project_id>/', views.update_project, name='update_project'),
    path('removeproject/<int:project_id>/', views.remove_project, name='removeproject'),
    path('work_experiences/', views.work_experience_list, name='work_experience_list'),
    path('work_experiences/add/', views.add_work_experience, name='add_work_experience'),
    path('work_experiences/remove/<int:pk>/', views.remove_work_experience, name='remove_work_experience'),
    path('certification/', views.certification_list, name='certification_list'),
    path('certification/add/', views.add_certification, name='add_certification'),
    path('certification/remove/<int:pk>/', views.remove_certification, name='remove_certification'),
]