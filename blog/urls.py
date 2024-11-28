from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index')

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
path('create/', views.create_post, name='create_post',
path('subscribe/<int:user_id>/', views.subscribe, name='subscribe'),
path('unsubscribe/<int:user_id>/', views.unsubscribe, name='unsubscribe'),
)
]

