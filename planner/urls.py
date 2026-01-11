from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("download-report/", views.download_report, name="download_report"),
    path("store-charts/", views.store_charts, name="store_charts"),
    path("download-report/", views.download_report, name="download_report"),

]

