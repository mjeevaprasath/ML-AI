from django.contrib import admin
from django.urls import path
from ai_ml_assistant import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login_page),
    path('login/', views.login_page, name='login'),

    path('signup/', views.signup_page, name='signup'),
    path('home/', views.home_page, name='home'),
    path('logout/', views.logout_page, name='logout'),
]