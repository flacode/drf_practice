from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('', views.api_root, name='api_root'),
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('posts/admin/', views.UserList.as_view(), name='user_list'),
    path('posts/admin/<int:pk>/', views.UserAdministration.as_view(), name='user_details'),
    path('posts/register/', views.UserRegistration.as_view(), name='register'),
    path('posts/user/<int:pk>/', views.UserView.as_view(), name='user_view'),
    path('posts/login/', obtain_jwt_token, name='login'),
]
