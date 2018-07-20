from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from . import views


urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('useradmin/', views.UserList.as_view()),
    path('useradmin/<int:pk>/', views.UserAdministration.as_view()),
    path('register/', views.UserRegistration.as_view()),
    path('user/<int:pk>/', views.UserView.as_view()),
    path('login/', obtain_jwt_token),
    path('auth/', include('rest_framework.urls'))
]
