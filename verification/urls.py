from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'myapp'

urlpatterns = [
    path('register/', views.User.as_view(), name='register'),
    path('verify/', views.VerifyView.as_view(), name='verify'),
    path('home/', views.UserAuth.as_view(), name='home'),

    path('post/', views.UserGetView.as_view(), name='post'),
    path('post/create/', views.UserCreateView.as_view(), name='create'),
    path('post/update/<slug:slug>/', views.UserUpdateView.as_view(), name='update'),
    path('post/delete/<slug:slug>/', views.UserdeleteView.as_view(), name='delete'),

    path('refresh/', TokenRefreshView.as_view())
#
]
