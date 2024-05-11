
from django.contrib import admin
from django.urls import path
from app02 import views#从名为app02的模块中导入views对象
#URL和视图函数的对应关系，在app的views中找到
urlpatterns = [

    path('login/user_add/',views.user_add),#访问就会触发这个函数
    path('login/',views.user_login),
    path('login/<str:username_>/home/',views.home),
    path('logout/', views.logout, name='logout'),
]
