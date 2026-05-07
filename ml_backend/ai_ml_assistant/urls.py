from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page),
    path('login/', views.login_page),
    path('signup/', views.signup_page),
    path('home/', views.home_page),
    path('logout/', views.logout_page),

    path('search/', views.search),

    path('lens/', views.lens_page),
    path('lens_api/', views.lens_api),

    path('mic/', views.mic),
    #path('vtube/', views.vtube_control),

    path('speak_api/', views.speak_api),

    #path("vtube/talk/",views.vtube_talk),
    #path("vtube/idle/",views.vtube_idle),

    path("hotkey",views.hotkey),

    path('process/', views.process),
    path('speak/',views.speak_api),
]