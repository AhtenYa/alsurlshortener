from django.urls import path

from . import views

app_name = 'muskers'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('user/', views.CreateCulinkView.as_view(), name='user'),
    path('user/shorts/', views.ResultsView.as_view(), name='shorts'),
    path('user/shorts/details/<slug:slug>/', views.CulinkDetailsView.as_view(), name='details'),
    path('user/shorts/edit/<slug:slug>/', views.CulinkUpdateView.as_view(), name='edit'),
    path('user/shorts/delete/<slug:slug>/', views.CulinkDeleteView.as_view(), name='delete'),
    path('user/settings/', views.UserUpdateView.as_view(), name='settings'),
    path('user/settings/password/', views.UserPasswordView.as_view(), name='password'),
    path('user/settings/delete/<slug:slug>/', views.UserDeleteView.as_view(), name='delete_user')
]
