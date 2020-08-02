from django.urls import path
from video import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index',views.index,name='index'),
    path('register', views.register, name='register'),
    path('logout',views.logout,name='logout'),
    path('login', views.login, name='login'),
    path('upload_video', views.upload_video, name='upload_video'),
    path('play_video<int:id>', views.play_video, name='play_video'),
    path('add_comment', views.add_comment, name='add_comment'),
]
