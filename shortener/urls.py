from django.urls import path

from . import views

app_name = 'shortener'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('r/<str:shortlink>/', views.check_link),
    path('<str:shortlink>/', views.redirect_to)
]
