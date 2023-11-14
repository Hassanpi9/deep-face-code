from django.urls import path
from . import views

urlpatterns = [
    path('api/users/', views.UserListCreateView.as_view()),
    path('api/users/<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view())
]
