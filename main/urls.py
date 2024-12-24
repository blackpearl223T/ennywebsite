from django.urls import path
from . import views 

urlpatterns = [
    path('', views.redirect_to_home, name='root'),
    path("<int:id>",views.index, name="index"),
    path("create/",views.create, name="create"),
    path("home/",views.home, name="home"),
    path("view/",views.view, name="view"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
] 