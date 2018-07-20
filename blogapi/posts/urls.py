from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('useradmin/', views.UserList.as_view()),
    path('useradmin/<int:pk>/', views.UserAdministration.as_view()),
    path('register/', views.UserRegistration.as_view()),
    path('user/<int:pk>/', views.UserView.as_view()),
]
